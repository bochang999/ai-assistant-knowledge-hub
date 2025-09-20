# Injection Attack Prevention Patterns

## 🚨 Critical Priority: Injection Attack Prevention

Injection attacks are among the most dangerous vulnerabilities in Python applications. They occur when untrusted input is passed to an interpreter as part of a command or query.

---

## Command Injection Prevention

### ❌ DANGEROUS PATTERNS

```python
import os
import subprocess

# NEVER DO THIS - Command injection vulnerability
user_file = request.args.get('filename')
os.system(f'cat {user_file}')  # ❌ CRITICAL VULNERABILITY

# NEVER DO THIS - Shell injection
subprocess.call(f'grep "{search_term}" {filename}', shell=True)  # ❌ DANGEROUS

# NEVER DO THIS - Eval injection
user_code = request.json.get('expression')
result = eval(user_code)  # ❌ EXTREMELY DANGEROUS
```

### ✅ SECURE PATTERNS

```python
import subprocess
import shlex
from pathlib import Path

# ✅ SECURE - Use argument lists
def safe_file_read(filename):
    # Validate filename first
    safe_path = Path('/safe/directory') / Path(filename).name
    try:
        subprocess.run(['cat', str(safe_path)], check=True, capture_output=True)
    except subprocess.CalledProcessError:
        return None

# ✅ SECURE - Parameterized subprocess
def safe_grep(search_term, filename):
    # Validate inputs
    safe_filename = Path(filename).name
    return subprocess.run(
        ['grep', search_term, safe_filename],
        capture_output=True,
        text=True,
        check=False
    )

# ✅ SECURE - Safe evaluation alternatives
import ast
def safe_eval(expression):
    try:
        # Only allow literal expressions
        return ast.literal_eval(expression)
    except (ValueError, SyntaxError):
        raise ValueError("Invalid expression")
```

---

## SQL Injection Prevention

### ❌ DANGEROUS PATTERNS

```python
import sqlite3

# NEVER DO THIS - SQL injection vulnerability
user_id = request.args.get('id')
cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")  # ❌ CRITICAL

# NEVER DO THIS - String concatenation
query = "SELECT * FROM products WHERE name = '" + product_name + "'"  # ❌ DANGEROUS
cursor.execute(query)

# NEVER DO THIS - Format strings
cursor.execute("DELETE FROM users WHERE role = '{}'".format(role))  # ❌ DANGEROUS
```

### ✅ SECURE PATTERNS

```python
import sqlite3
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

# ✅ SECURE - Parameterized queries (sqlite3)
def get_user_secure(user_id):
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()

# ✅ SECURE - Named parameters
def get_products_secure(category, min_price):
    cursor.execute(
        "SELECT * FROM products WHERE category = :cat AND price >= :price",
        {"cat": category, "price": min_price}
    )
    return cursor.fetchall()

# ✅ SECURE - SQLAlchemy ORM
def get_user_orm(session, user_id):
    return session.query(User).filter(User.id == user_id).first()

# ✅ SECURE - SQLAlchemy with text() for complex queries
def complex_query_secure(session, status):
    return session.execute(
        text("SELECT * FROM orders WHERE status = :status"),
        {"status": status}
    ).fetchall()
```

---

## Code Injection Prevention

### ❌ DANGEROUS PATTERNS

```python
# NEVER DO THIS - Arbitrary code execution
user_function = request.json.get('function')
exec(user_function)  # ❌ EXTREMELY DANGEROUS

# NEVER DO THIS - Dynamic imports
module_name = request.args.get('module')
imported = __import__(module_name)  # ❌ DANGEROUS

# NEVER DO THIS - Compile and execute
code = request.json.get('code')
compiled = compile(code, '<string>', 'exec')
exec(compiled)  # ❌ EXTREMELY DANGEROUS
```

### ✅ SECURE PATTERNS

```python
import ast
import operator
import math

# ✅ SECURE - Whitelist approach for calculations
ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.USub: operator.neg,
}

ALLOWED_FUNCTIONS = {
    'abs': abs,
    'max': max,
    'min': min,
    'round': round,
    'sqrt': math.sqrt,
}

def safe_eval_math(expression):
    """Safely evaluate mathematical expressions"""
    try:
        tree = ast.parse(expression, mode='eval')
        return eval_ast_node(tree.body)
    except:
        raise ValueError("Invalid mathematical expression")

def eval_ast_node(node):
    if isinstance(node, ast.Constant):  # Numbers, strings
        return node.value
    elif isinstance(node, ast.BinOp):
        left = eval_ast_node(node.left)
        right = eval_ast_node(node.right)
        return ALLOWED_OPERATORS[type(node.op)](left, right)
    elif isinstance(node, ast.UnaryOp):
        operand = eval_ast_node(node.operand)
        return ALLOWED_OPERATORS[type(node.op)](operand)
    elif isinstance(node, ast.Call):
        if node.func.id in ALLOWED_FUNCTIONS:
            args = [eval_ast_node(arg) for arg in node.args]
            return ALLOWED_FUNCTIONS[node.func.id](*args)
    raise ValueError("Unsupported operation")

# ✅ SECURE - Predefined function dispatch
ALLOWED_ACTIONS = {
    'calculate_tax': lambda amount: amount * 0.1,
    'format_currency': lambda amount: f"${amount:.2f}",
    'validate_email': lambda email: '@' in email and '.' in email.split('@')[1]
}

def safe_action_dispatch(action_name, *args):
    if action_name in ALLOWED_ACTIONS:
        return ALLOWED_ACTIONS[action_name](*args)
    raise ValueError("Action not allowed")
```

---

## Template Injection Prevention

### ❌ DANGEROUS PATTERNS

```python
from jinja2 import Template

# NEVER DO THIS - Template injection
user_template = request.json.get('template')
template = Template(user_template)  # ❌ DANGEROUS
result = template.render(user_data=data)

# NEVER DO THIS - String formatting injection
template_string = request.json.get('format')
result = template_string.format(**user_data)  # ❌ DANGEROUS
```

### ✅ SECURE PATTERNS

```python
from jinja2 import Environment, DictLoader, select_autoescape
from string import Template

# ✅ SECURE - Pre-defined templates only
SAFE_TEMPLATES = {
    'welcome': 'Welcome, {{ username }}!',
    'notification': 'You have {{ count }} new messages',
    'invoice': 'Total: ${{ amount }}'
}

env = Environment(
    loader=DictLoader(SAFE_TEMPLATES),
    autoescape=select_autoescape(['html', 'xml'])
)

def safe_template_render(template_name, **kwargs):
    if template_name not in SAFE_TEMPLATES:
        raise ValueError("Template not allowed")

    template = env.get_template(template_name)
    return template.render(**kwargs)

# ✅ SECURE - String Template with validation
def safe_string_format(template_name, **kwargs):
    if template_name not in SAFE_TEMPLATES:
        raise ValueError("Template not allowed")

    template = Template(SAFE_TEMPLATES[template_name])
    return template.safe_substitute(**kwargs)
```

---

## LDAP Injection Prevention

### ❌ DANGEROUS PATTERNS

```python
import ldap

# NEVER DO THIS - LDAP injection
user_input = request.args.get('username')
search_filter = f"(uid={user_input})"  # ❌ DANGEROUS
```

### ✅ SECURE PATTERNS

```python
import ldap
import ldap.filter

# ✅ SECURE - Proper LDAP escaping
def safe_ldap_search(username):
    # Escape special LDAP characters
    safe_username = ldap.filter.escape_filter_chars(username)
    search_filter = f"(uid={safe_username})"
    return search_filter
```

---

## General Injection Prevention Guidelines

### Input Validation Strategy

```python
import re
from typing import Union

class InputValidator:
    @staticmethod
    def validate_alphanumeric(value: str, max_length: int = 50) -> bool:
        """Validate alphanumeric input with length limit"""
        if not isinstance(value, str) or len(value) > max_length:
            return False
        return re.match(r'^[a-zA-Z0-9_-]+$', value) is not None

    @staticmethod
    def validate_email(email: str) -> bool:
        """Basic email validation"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    @staticmethod
    def validate_filename(filename: str) -> bool:
        """Validate safe filename"""
        if not filename or '..' in filename or '/' in filename:
            return False
        return re.match(r'^[a-zA-Z0-9._-]+$', filename) is not None

    @staticmethod
    def sanitize_sql_identifier(identifier: str) -> Union[str, None]:
        """Sanitize SQL identifier (table name, column name)"""
        if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', identifier):
            return None
        return identifier
```

### Error Handling Best Practices

```python
import logging

def secure_error_handler(func):
    """Decorator for secure error handling"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # Log full error details securely
            logging.error(f"Function {func.__name__} failed: {str(e)}", exc_info=True)

            # Return generic error to user
            raise ValueError("Invalid input provided")
    return wrapper

@secure_error_handler
def process_user_data(data):
    # Your processing logic here
    pass
```

---

## Automated Detection Rules

These patterns can be automatically detected by the security context injector:

```regex
# Command injection patterns
os\.system\s*\(.*\{.*\}
subprocess\.call\s*\(.*shell\s*=\s*True
eval\s*\(
exec\s*\(

# SQL injection patterns
\.execute\s*\(.*f["'].*\{
\.execute\s*\(.*\+.*\)
\.execute\s*\(.*\.format\s*\(

# Code injection patterns
__import__\s*\(
compile\s*\(.*exec
exec\s*\(.*input
eval\s*\(.*input
```

**🎯 Remember: The best defense against injection attacks is to never trust user input and always use parameterized queries, whitelisting, and proper input validation.**
