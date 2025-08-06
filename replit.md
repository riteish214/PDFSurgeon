# DocMorph - Dark Theme Web Application

## Project Overview
A full-stack dark-themed web application built with Flask that provides comprehensive PDF processing tools and secure file sharing capabilities. The application features a modern dark UI with neon blue/green accent colors and supports PDF manipulation, file conversion, and secure sharing with QR codes.

## User Preferences
- **Theme**: Dark theme with black background and orange (#FF7F11) accent colors
- **No PDF editing functionality** - explicitly requested by user
- **Design**: Modern, professional interface with TailwindCSS
- **Security**: Focus on secure file sharing with expiration and password protection

## Project Architecture

### Backend (Flask)
- **Framework**: Flask with SQLAlchemy ORM
- **Database**: PostgreSQL with models for Users, SharedFiles, and PDFProcessingJobs
- **Authentication**: Flask-Login for user management
- **File Processing**: PyPDF2, pdfplumber, reportlab for PDF operations
- **File Sharing**: Unique access codes, QR code generation, expiration controls

### Frontend
- **Styling**: TailwindCSS with custom dark theme configuration
- **JavaScript**: Vanilla JS for drag-and-drop file handling and API interactions
- **Icons**: Font Awesome for consistent iconography
- **Responsive**: Mobile-first design with responsive layouts

### Key Features
1. **PDF Processing Tools**:
   - Merge multiple PDFs
   - Split PDF into individual pages
   - Compress PDF files
   - Encrypt/decrypt with password protection

2. **File Conversion**:
   - PDF ↔ DOCX
   - PDF ↔ TXT
   - PDF ↔ CSV
   - Support for batch processing

3. **Secure File Sharing**:
   - Unique 8-character access codes
   - QR code generation for easy sharing
   - Expiration times (1 hour to 1 week)
   - Optional password protection
   - Download limits
   - Anonymous and registered user support

### File Structure
```
├── app.py              # Main Flask application
├── models.py           # Database models
├── utils/              # Utility modules
│   ├── pdf_processor.py    # PDF processing logic
│   ├── file_converter.py   # File conversion utilities
│   └── qr_generator.py     # QR code generation
├── templates/          # Jinja2 templates
│   ├── base.html           # Base template with dark theme
│   ├── index.html          # Landing page
│   ├── tools.html          # PDF tools interface
│   ├── share.html          # File sharing interface
│   ├── auth/               # Authentication templates
│   ├── shared/             # Shared file access templates
│   └── errors/             # Error page templates
└── static/             # Static assets
    ├── css/custom.css      # Custom styling
    └── js/                 # JavaScript modules
        ├── tools.js        # PDF tools functionality
        └── share.js        # File sharing functionality
```

## Recent Changes (2025-08-06)
- **Migration completed**: Successfully migrated from Replit Agent to standard Replit environment
- **Database setup**: PostgreSQL database configured with comprehensive models
- **Backend API**: Complete REST API for PDF processing and file sharing
- **Dark theme UI**: Full TailwindCSS implementation with neon accent colors
- **File sharing**: QR code generation and secure sharing system implemented
- **Authentication**: User registration and login system with Flask-Login
- **Error handling**: Comprehensive error pages and user feedback

## Technical Decisions
1. **Database**: PostgreSQL chosen for robust data persistence and relationships
2. **PDF Processing**: PyPDF2 and pdfplumber for reliable PDF manipulation
3. **QR Codes**: Python qrcode library with custom styling
4. **File Storage**: Local filesystem with organized folder structure
5. **Security**: Werkzeug password hashing, unique access codes, expiration controls
6. **UI Framework**: TailwindCSS for rapid, consistent styling

## Dependencies
- Flask ecosystem (Flask, Flask-SQLAlchemy, Flask-Login, Flask-Migrate)
- PDF processing (PyPDF2, pdfplumber, reportlab)
- File handling (python-docx, pandas)
- QR codes (qrcode[pil])
- Security (bcrypt, werkzeug)

## Deployment Notes
- Application runs on port 5000 with Gunicorn
- Environment variables: DATABASE_URL, SESSION_SECRET
- File uploads limited to 100MB
- Temporary files cleaned up after processing
- QR codes and shared files stored in organized directories

## Current Status
✅ **COMPLETED**: Full-stack PDF tools application with dark theme UI
- All PDF processing tools functional
- Secure file sharing with QR codes implemented
- Authentication system working
- Dark theme UI with neon accents deployed
- Application running and accessible