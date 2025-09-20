# Python Security Context Templates

## 🔒 Auto-Injection Security Context Templates

These templates are automatically injected into Claude's context when Python development is detected, based on project risk level and code patterns.

---

### HIGH RISK SECURITY CONTEXT

**Auto-triggers:** Web applications, API development, file upload/processing, database operations, user authentication

```markdown
🚨 HIGH RISK PYTHON DEVELOPMENT DETECTED 🚨

MANDATORY SECURITY REQUIREMENTS:
✅ ALL user inputs MUST be validated and sanitized
✅ Database queries MUST use parameterized statements
✅ File operations MUST validate paths and file types
✅ Error messages MUST NOT leak sensitive information
✅ Authentication MUST use secure hashing (SHA-256+)

PROHIBITED FUNCTIONS:
❌ os.system() with user input
❌ eval() or exec() with untrusted data
❌ pickle.loads() on external data
❌ SQL string concatenation
❌ MD5 or SHA1 for passwords

BEFORE GENERATING CODE:
1. Identify all user input points
2. Plan validation strategy for each input
3. Choose secure alternatives for high-risk operations
4. Design proper error handling

CODE REVIEW REQUIRED: All generated code must be reviewed for security vulnerabilities before implementation.
```

---

### MEDIUM RISK SECURITY CONTEXT

**Auto-triggers:** Automation scripts, data processing, system integration, file manipulation

```markdown
⚠️ MEDIUM RISK PYTHON DEVELOPMENT DETECTED ⚠️

SECURITY GUIDELINES:
✅ Validate file paths to prevent directory traversal
✅ Use subprocess with argument lists, not shell=True
✅ Implement proper exception handling
✅ Sanitize any external input or data

WATCH OUT FOR:
🔍 Command injection via os.system()
🔍 Path traversal in file operations
🔍 Unsafe deserialization
🔍 Unvalidated external input

SECURE CODING:
- Use pathlib.Path().resolve() for safe path handling
- Prefer subprocess.run([cmd, arg1, arg2]) over shell commands
- Use json.loads() instead of pickle.loads() when possible
- Validate and limit file operations to intended directories
```

---

### CRYPTOGRAPHY SECURITY CONTEXT

**Auto-triggers:** encryption, hashing, password, authentication, token, security, crypto

```markdown
🔐 CRYPTOGRAPHY SECURITY REQUIREMENTS 🔐

MANDATORY CRYPTO STANDARDS:
✅ Use SHA-256 or stronger for hashing (never MD5/SHA1)
✅ Use secrets.SystemRandom() for cryptographic randomness
✅ Use established crypto libraries (cryptography, bcrypt)
✅ Implement proper key management
✅ Use secure random for salts and tokens

PROHIBITED CRYPTO PRACTICES:
❌ hashlib.md5() or hashlib.sha1() for security purposes
❌ random.random() for crypto operations
❌ Hardcoded encryption keys
❌ ECB mode encryption
❌ Custom crypto implementations

RECOMMENDED LIBRARIES:
- bcrypt for password hashing
- cryptography library for encryption
- secrets module for random generation
- PyJWT for JWT tokens (with proper validation)

EXAMPLE SECURE PATTERNS:
```python
# Secure password hashing
import bcrypt
password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# Secure random token generation
import secrets
token = secrets.token_urlsafe(32)

# Secure file encryption
from cryptography.fernet import Fernet
key = Fernet.generate_key()
cipher = Fernet(key)
```
```

---

### WEB SCRAPING SECURITY CONTEXT

**Auto-triggers:** requests, urllib, web scraping, API calls, HTTP

```markdown
🌐 WEB SCRAPING SECURITY REQUIREMENTS 🌐

SSRF PROTECTION:
✅ Validate and whitelist target URLs/domains
✅ Set request timeouts and size limits
✅ Use proper SSL certificate verification
✅ Implement rate limiting

SECURE REQUEST PATTERNS:
```python
import requests
from urllib.parse import urlparse

# Validate URL before requesting
def is_safe_url(url):
    parsed = urlparse(url)
    return parsed.scheme in ['http', 'https'] and parsed.netloc in ALLOWED_DOMAINS

if is_safe_url(target_url):
    response = requests.get(target_url, timeout=10, verify=True)
```

AVOID:
❌ Requesting user-provided URLs without validation
❌ Disabling SSL verification (verify=False)
❌ Unlimited request sizes or timeouts
❌ Following redirects to internal networks
```

---

### DATABASE SECURITY CONTEXT

**Auto-triggers:** SQL, database, cursor, sqlite, mysql, postgres, mongodb

```markdown
💾 DATABASE SECURITY REQUIREMENTS 💾

SQL INJECTION PREVENTION:
✅ ALWAYS use parameterized queries
✅ NEVER concatenate user input into SQL strings
✅ Use ORM query builders when possible
✅ Validate input types and ranges

SECURE DATABASE PATTERNS:
```python
# ✅ SECURE - Parameterized query
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))

# ✅ SECURE - ORM usage
user = User.objects.filter(id=user_id).first()

# ❌ DANGEROUS - String concatenation
cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
```

CONNECTION SECURITY:
✅ Use SSL/TLS for database connections
✅ Store credentials securely (environment variables)
✅ Implement connection pooling and limits
✅ Use least-privilege database accounts
```

---

### FILE PROCESSING SECURITY CONTEXT

**Auto-triggers:** file upload, open(), pathlib, shutil, file processing

```markdown
📁 FILE PROCESSING SECURITY REQUIREMENTS 📁

PATH TRAVERSAL PREVENTION:
✅ Validate file paths with os.path.basename()
✅ Use pathlib.Path().resolve() to resolve relative paths
✅ Restrict operations to designated directories
✅ Validate file extensions and MIME types

SECURE FILE PATTERNS:
```python
import os
from pathlib import Path

# ✅ SECURE - Path validation
def safe_file_path(filename, base_dir):
    safe_name = os.path.basename(filename)
    full_path = Path(base_dir) / safe_name
    return full_path.resolve()

# ✅ SECURE - File type validation
ALLOWED_EXTENSIONS = {'.txt', '.csv', '.json'}
if Path(filename).suffix.lower() in ALLOWED_EXTENSIONS:
    # Process file
```

FILE UPLOAD SECURITY:
✅ Limit file sizes (max 10MB for most cases)
✅ Scan uploaded files for malware
✅ Store uploads outside web root
✅ Generate unique filenames to prevent conflicts
```

---

## Context Injection Rules

### Automatic Activation
1. **Project Detection**: Analyze project structure and dependencies
2. **Intent Analysis**: Parse user requests for security-relevant keywords
3. **File Operations**: Monitor file extension and operation patterns
4. **Risk Assessment**: Combine factors to determine appropriate security context

### Manual Override
```bash
# Force high-security context
export PYTHON_SECURITY_LEVEL=HIGH

# Disable security context (not recommended)
export PYTHON_SECURITY_LEVEL=NONE
```

### Integration with Linear Workflow
- Security context activation is logged to Linear issues
- Security violations trigger automatic issue comments
- Compliance checklists are attached to relevant issues
- Security reviews are tracked in issue status updates
