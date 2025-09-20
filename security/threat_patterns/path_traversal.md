# Path Traversal Attack Prevention Patterns

## 🚨 High Priority: Path Traversal Prevention

Path traversal attacks allow attackers to access files and directories outside the intended scope by manipulating file paths with sequences like `../` or absolute paths.

---

## File Access Vulnerabilities

### ❌ DANGEROUS PATTERNS

```python
import os
from pathlib import Path

# NEVER DO THIS - Direct file path concatenation
user_file = request.args.get('filename')
file_path = f'/uploads/{user_file}'  # ❌ DANGEROUS
with open(file_path, 'r') as f:
    content = f.read()

# NEVER DO THIS - os.path.join without validation
filename = request.form.get('file')
full_path = os.path.join('/safe/directory', filename)  # ❌ DANGEROUS
os.remove(full_path)

# NEVER DO THIS - Direct path construction
image_name = request.args.get('image')
image_path = '/var/www/images/' + image_name  # ❌ DANGEROUS
```

### ✅ SECURE PATTERNS

```python
import os
from pathlib import Path

# ✅ SECURE - Path validation and sanitization
def safe_file_access(filename, base_directory='/uploads'):
    """Safely access files within a designated directory"""
    # Remove any path components, keep only filename
    safe_name = os.path.basename(filename)

    # Construct safe path
    base_path = Path(base_directory).resolve()
    file_path = (base_path / safe_name).resolve()

    # Ensure the resolved path is still within base directory
    if not str(file_path).startswith(str(base_path)):
        raise ValueError("Invalid file path")

    return file_path

# ✅ SECURE - Using pathlib with validation
def secure_file_read(filename, allowed_dir='/safe/uploads'):
    """Securely read file with path validation"""
    try:
        # Sanitize filename
        clean_name = Path(filename).name

        # Build safe path
        safe_path = Path(allowed_dir) / clean_name
        resolved_path = safe_path.resolve()

        # Verify path is within allowed directory
        allowed_path = Path(allowed_dir).resolve()
        if not str(resolved_path).startswith(str(allowed_path)):
            raise PermissionError("Access denied")

        # Additional file existence and permission checks
        if not resolved_path.exists():
            raise FileNotFoundError("File not found")

        if not resolved_path.is_file():
            raise ValueError("Not a regular file")

        return resolved_path.read_text(encoding='utf-8')

    except Exception as e:
        logging.warning(f"File access denied for {filename}: {e}")
        raise PermissionError("File access denied")
```

---

## Directory Traversal Prevention

### ❌ DANGEROUS PATTERNS

```python
# NEVER DO THIS - Unvalidated directory listing
directory = request.args.get('dir')
files = os.listdir(f'/data/{directory}')  # ❌ DANGEROUS

# NEVER DO THIS - Archive extraction without validation
import zipfile
with zipfile.ZipFile(uploaded_file) as zip_ref:
    zip_ref.extractall('/temp/')  # ❌ ZIP BOMB / PATH TRAVERSAL

# NEVER DO THIS - File copying without validation
source = request.form.get('source')
destination = request.form.get('dest')
shutil.copy(source, destination)  # ❌ DANGEROUS
```

### ✅ SECURE PATTERNS

```python
import os
import zipfile
import shutil
from pathlib import Path

# ✅ SECURE - Safe directory listing
def safe_directory_listing(subdir, base_dir='/safe/data'):
    """Safely list directory contents"""
    # Sanitize subdirectory name
    clean_subdir = os.path.basename(subdir) if subdir else ''

    # Build and validate path
    target_path = Path(base_dir) / clean_subdir
    resolved_path = target_path.resolve()
    base_path = Path(base_dir).resolve()

    # Ensure we're still within base directory
    if not str(resolved_path).startswith(str(base_path)):
        raise PermissionError("Directory access denied")

    if not resolved_path.is_dir():
        raise NotADirectoryError("Invalid directory")

    # Return only filenames, not full paths
    return [f.name for f in resolved_path.iterdir() if f.is_file()]

# ✅ SECURE - Safe archive extraction
def safe_extract_zip(zip_file, extract_to='/temp/uploads'):
    """Safely extract ZIP file with path validation"""
    extract_path = Path(extract_to).resolve()

    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        for member in zip_ref.infolist():
            # Validate each file path in the archive
            if not is_safe_extract_path(member.filename, extract_path):
                raise ValueError(f"Unsafe path in archive: {member.filename}")

            # Additional size check (ZIP bomb protection)
            if member.file_size > 100 * 1024 * 1024:  # 100MB limit
                raise ValueError(f"File too large: {member.filename}")

        # Safe to extract
        zip_ref.extractall(extract_path)

def is_safe_extract_path(filename, base_path):
    """Check if extraction path is safe"""
    # Remove leading slash and normalize
    clean_filename = filename.lstrip('/')
    target_path = (base_path / clean_filename).resolve()

    # Ensure target is within base directory
    return str(target_path).startswith(str(base_path))

# ✅ SECURE - Safe file copying
def safe_file_copy(source_name, dest_name, base_dir='/safe/files'):
    """Safely copy files within allowed directory"""
    base_path = Path(base_dir).resolve()

    # Sanitize filenames
    clean_source = os.path.basename(source_name)
    clean_dest = os.path.basename(dest_name)

    # Build paths
    source_path = (base_path / clean_source).resolve()
    dest_path = (base_path / clean_dest).resolve()

    # Validate both paths are within base directory
    for path in [source_path, dest_path]:
        if not str(path).startswith(str(base_path)):
            raise PermissionError("File operation outside allowed directory")

    # Perform safe copy
    shutil.copy2(source_path, dest_path)
```

---

## URL/Web Path Vulnerabilities

### ❌ DANGEROUS PATTERNS

```python
from flask import Flask, request, send_file

app = Flask(__name__)

# NEVER DO THIS - Direct file serving
@app.route('/download/<filename>')
def download_file(filename):
    return send_file(f'/files/{filename}')  # ❌ DANGEROUS

# NEVER DO THIS - Template path injection
@app.route('/template/<template_name>')
def render_template(template_name):
    return render_template(f'{template_name}.html')  # ❌ DANGEROUS
```

### ✅ SECURE PATTERNS

```python
from flask import Flask, request, send_file, abort
import os
from pathlib import Path

app = Flask(__name__)

# ✅ SECURE - Validated file serving
ALLOWED_FILES_DIR = Path('/safe/downloads').resolve()
ALLOWED_EXTENSIONS = {'.txt', '.pdf', '.jpg', '.png', '.zip'}

@app.route('/download/<filename>')
def secure_download(filename):
    """Securely serve files with validation"""
    try:
        # Sanitize filename
        clean_filename = os.path.basename(filename)

        # Check file extension
        file_ext = Path(clean_filename).suffix.lower()
        if file_ext not in ALLOWED_EXTENSIONS:
            abort(403)  # Forbidden

        # Build safe path
        file_path = (ALLOWED_FILES_DIR / clean_filename).resolve()

        # Verify path is within allowed directory
        if not str(file_path).startswith(str(ALLOWED_FILES_DIR)):
            abort(403)

        # Check file exists and is regular file
        if not file_path.exists() or not file_path.is_file():
            abort(404)

        return send_file(file_path, as_attachment=True)

    except Exception:
        abort(500)

# ✅ SECURE - Template whitelist
ALLOWED_TEMPLATES = {
    'home': 'home.html',
    'about': 'about.html',
    'contact': 'contact.html'
}

@app.route('/page/<page_name>')
def render_page(page_name):
    """Securely render templates from whitelist"""
    if page_name not in ALLOWED_TEMPLATES:
        abort(404)

    template_file = ALLOWED_TEMPLATES[page_name]
    return render_template(template_file)
```

---

## Configuration File Vulnerabilities

### ❌ DANGEROUS PATTERNS

```python
# NEVER DO THIS - User-controlled config file access
config_file = request.args.get('config')
with open(f'/configs/{config_file}', 'r') as f:
    config = f.read()

# NEVER DO THIS - Include/require with user input
include_file = request.form.get('include')
exec(open(include_file).read())  # ❌ EXTREMELY DANGEROUS
```

### ✅ SECURE PATTERNS

```python
import json
from pathlib import Path

# ✅ SECURE - Predefined configuration options
ALLOWED_CONFIGS = {
    'database': '/configs/database.json',
    'logging': '/configs/logging.json',
    'api': '/configs/api.json'
}

def load_config(config_name):
    """Safely load predefined configuration"""
    if config_name not in ALLOWED_CONFIGS:
        raise ValueError("Invalid configuration name")

    config_path = Path(ALLOWED_CONFIGS[config_name])

    # Verify file exists and is within expected location
    if not config_path.exists():
        raise FileNotFoundError("Configuration file not found")

    # Load and validate JSON
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        raise ValueError("Invalid configuration format")

# ✅ SECURE - Configuration validation
def validate_config_structure(config_data, required_fields):
    """Validate configuration structure"""
    for field in required_fields:
        if field not in config_data:
            raise ValueError(f"Missing required field: {field}")

    return True
```

---

## File Upload Security

### ❌ DANGEROUS PATTERNS

```python
from flask import request

# NEVER DO THIS - Unrestricted file upload
@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    file.save(f'/uploads/{file.filename}')  # ❌ DANGEROUS
```

### ✅ SECURE PATTERNS

```python
import os
import uuid
from pathlib import Path
from werkzeug.utils import secure_filename

# ✅ SECURE - Safe file upload
UPLOAD_DIR = Path('/safe/uploads').resolve()
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
ALLOWED_EXTENSIONS = {'.txt', '.pdf', '.jpg', '.jpeg', '.png', '.gif'}

@app.route('/upload', methods=['POST'])
def secure_upload():
    """Securely handle file uploads"""
    if 'file' not in request.files:
        return "No file provided", 400

    file = request.files['file']
    if file.filename == '':
        return "No file selected", 400

    # Validate file size
    file.seek(0, 2)  # Seek to end
    file_size = file.tell()
    file.seek(0)  # Reset to beginning

    if file_size > MAX_FILE_SIZE:
        return "File too large", 413

    # Secure filename handling
    original_filename = secure_filename(file.filename)
    file_ext = Path(original_filename).suffix.lower()

    # Validate file extension
    if file_ext not in ALLOWED_EXTENSIONS:
        return "File type not allowed", 400

    # Generate unique filename to prevent conflicts
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    file_path = UPLOAD_DIR / unique_filename

    # Save file
    file.save(file_path)

    return f"File uploaded successfully as {unique_filename}", 200
```

---

## Path Validation Utilities

```python
import os
from pathlib import Path
from typing import Union

class PathValidator:
    """Utility class for path validation"""

    @staticmethod
    def is_safe_path(path: Union[str, Path], base_dir: Union[str, Path]) -> bool:
        """Check if path is safe within base directory"""
        try:
            path = Path(path).resolve()
            base = Path(base_dir).resolve()
            return str(path).startswith(str(base))
        except (OSError, ValueError):
            return False

    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """Sanitize filename by removing directory components"""
        return os.path.basename(filename)

    @staticmethod
    def validate_file_extension(filename: str, allowed_extensions: set) -> bool:
        """Validate file extension against allowed list"""
        ext = Path(filename).suffix.lower()
        return ext in allowed_extensions

    @staticmethod
    def build_safe_path(filename: str, base_dir: str) -> Path:
        """Build a safe file path within base directory"""
        clean_name = PathValidator.sanitize_filename(filename)
        path = (Path(base_dir) / clean_name).resolve()

        if not PathValidator.is_safe_path(path, base_dir):
            raise ValueError("Unsafe file path")

        return path

# Example usage
validator = PathValidator()

def secure_file_operation(filename, base_dir='/safe/files'):
    """Example of secure file operation"""
    if not validator.validate_file_extension(filename, {'.txt', '.csv'}):
        raise ValueError("Invalid file type")

    safe_path = validator.build_safe_path(filename, base_dir)
    return safe_path
```

---

## Automated Detection Rules

These patterns can be detected by security scanners:

```regex
# Path traversal patterns
\.\./
/\.\./
\.\.\\
\\\.\.\\

# Dangerous file operations
open\s*\(.*\+.*\)
os\.path\.join\s*\(.*request
shutil\.\w+\s*\(.*request

# Unsafe file serving
send_file\s*\(.*request
render_template\s*\(.*\+

# Archive extraction without validation
\.extractall\s*\(
```

**🎯 Key Principle: Always validate, sanitize, and confine file operations to designated safe directories. Never trust user-provided file paths.**
