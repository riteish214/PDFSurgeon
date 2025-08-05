# PDF Tools Suite

A comprehensive web-based PDF manipulation toolkit built with Flask that provides essential document processing capabilities. The application offers a clean, user-friendly interface for merging, splitting, converting, compressing, rotating, and securing PDF documents.

## Features

### Core PDF Operations
- **Merge PDFs** - Combine multiple PDF files into a single document
- **Split PDFs** - Extract individual pages from PDF documents
- **Convert Files** - Convert between PDF, Word (DOC/DOCX), and PowerPoint (PPT/PPTX) formats
- **Compress PDFs** - Reduce file size while maintaining quality
- **Rotate Pages** - Rotate PDF pages to correct orientation
- **Secure PDFs** - Add password protection to documents

### Key Features
- Clean, professional dark theme interface
- Drag-and-drop file upload support
- File validation and size limits (100MB max)
- Responsive design for all devices
- Real-time file preview and progress indicators
- Secure temporary file handling with automatic cleanup
- Bootstrap 5 with custom styling

## Tech Stack

### Backend
- **Python 3.11** - Core programming language
- **Flask** - Lightweight web framework
- **Gunicorn** - WSGI HTTP Server for production

### PDF Processing Libraries
- **PyPDF2** - Core PDF manipulation (merge, split, rotate, encrypt)
- **pdf2docx** - PDF to Word document conversion
- **python-pptx** - PowerPoint file handling and creation
- **ReportLab** - PDF generation for demo conversions

### Frontend
- **HTML5 & CSS3** - Modern web standards
- **Bootstrap 5** - Responsive UI framework with dark theme
- **JavaScript (Vanilla)** - Client-side functionality
- **Font Awesome** - Icon library

### Development Tools
- **uv** - Fast Python package manager
- **Werkzeug** - WSGI utilities for secure file handling

## Project Structure

```
pdf-tools-app/
├── app.py                 # Main Flask application
├── main.py               # Application entry point
├── requirements.txt      # Python dependencies
├── pyproject.toml       # Project configuration
├── replit.md            # Project documentation
├── README.md            # This file
├── templates/           # Jinja2 HTML templates
│   ├── base.html        # Base template with navigation
│   ├── index.html       # Homepage with tool overview
│   ├── merge.html       # PDF merge interface
│   ├── split.html       # PDF split interface
│   ├── convert.html     # File conversion interface
│   ├── compress.html    # PDF compression interface
│   ├── rotate.html      # PDF rotation interface
│   └── secure.html      # PDF security interface
├── static/              # Static assets
│   ├── css/
│   │   └── custom.css   # Custom styling and themes
│   └── js/
│       └── main.js      # JavaScript functionality
├── utils/               # Utility modules
│   ├── pdf_tools.py     # PDF processing operations
│   └── file_handler.py  # File upload and management
└── uploads/             # Temporary file storage
```

## Installation & Setup

### Prerequisites
- Python 3.11+
- uv package manager

### Local Development
1. Clone the repository
2. Install dependencies:
   ```bash
   uv add PyPDF2 pdf2docx python-pptx reportlab flask werkzeug gunicorn
   ```
3. Run the application:
   ```bash
   python main.py
   ```
4. Access at `http://localhost:5000`

### Production Deployment
The application is configured to run with Gunicorn:
```bash
gunicorn --bind 0.0.0.0:5000 --reuse-port --reload main:app
```

## Configuration

### File Limits
- Maximum file size: 100MB per file
- Supported formats: PDF, DOC, DOCX, PPT, PPTX
- Automatic cleanup of temporary files

### Security Features
- Secure filename handling with Werkzeug
- File type validation
- Temporary file isolation
- Password encryption for PDF protection

## API Endpoints

- `GET /` - Homepage with tool overview
- `GET /merge` - PDF merge interface
- `POST /api/merge` - Process PDF merge
- `GET /split` - PDF split interface
- `POST /api/split` - Process PDF split
- `GET /convert` - File conversion interface
- `POST /api/convert` - Process file conversion
- `GET /compress` - PDF compression interface
- `POST /api/compress` - Process PDF compression
- `GET /rotate` - PDF rotation interface
- `POST /api/rotate` - Process PDF rotation
- `GET /secure` - PDF security interface
- `POST /api/secure` - Process PDF encryption

## Browser Support

- Chrome/Chromium 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## License

This project is open source and available under the MIT License.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Support

For issues and feature requests, please create an issue in the repository.