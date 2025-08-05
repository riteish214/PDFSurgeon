# Local Setup Guide - PDF Tools Suite

## Quick Setup Instructions

### 1. Create Project Directory
```bash
mkdir pdf-tools-app
cd pdf-tools-app
```

### 2. Install Python Dependencies
```bash
pip install flask==3.1.1 PyPDF2==3.0.1 pdf2docx==0.5.8 python-pptx==1.0.2 reportlab==4.4.3 werkzeug==3.1.3 gunicorn==21.2.0
```

### 3. Create File Structure
```bash
mkdir templates static static/css static/js utils uploads
```

### 4. Copy Files
Copy these files from Replit to your local directory:
- `app.py` (main Flask application)
- `main.py` (entry point)
- `templates/` folder (all 8 HTML files)
- `static/css/custom.css`
- `static/js/main.js`
- `utils/pdf_tools.py`
- `utils/file_handler.py`

### 5. Run Locally
```bash
python main.py
```
Then open http://localhost:5000

## Alternative: requirements.txt
Create a `requirements.txt` file with:
```
Flask==3.1.1
PyPDF2==3.0.1
pdf2docx==0.5.8
python-pptx==1.0.2
reportlab==4.4.3
Werkzeug==3.1.3
gunicorn==21.2.0
```

Then install with:
```bash
pip install -r requirements.txt
```

## File List to Copy
1. `app.py` - Main application (254 lines)
2. `main.py` - Entry point (4 lines)
3. `templates/base.html` - Base template (107 lines)
4. `templates/index.html` - Homepage (141 lines)
5. `templates/merge.html` - Merge interface (116 lines)
6. `templates/split.html` - Split interface (108 lines)
7. `templates/convert.html` - Convert interface (162 lines)
8. `templates/compress.html` - Compress interface (124 lines)
9. `templates/rotate.html` - Rotate interface (168 lines)
10. `templates/secure.html` - Security interface (216 lines)
11. `static/css/custom.css` - Custom styles (154 lines)
12. `static/js/main.js` - JavaScript (254 lines)
13. `utils/pdf_tools.py` - PDF operations (339 lines)
14. `utils/file_handler.py` - File handling (266 lines)

Total: ~2,400 lines of code across 14 files
```

The most efficient way would be to manually copy each file since the project is relatively small (14 files). Would you like me to help you with any specific part of setting it up locally?