# PDF Tools Suite

## Overview

A comprehensive web-based PDF manipulation toolkit built with Flask that provides essential document processing capabilities. The application offers a clean, user-friendly interface for merging, splitting, converting, compressing, rotating, and securing PDF documents. It supports multiple file formats including PDF, Word documents (DOC/DOCX), and PowerPoint presentations (PPT/PPTX), making it a versatile solution for document management tasks.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Template Engine**: Jinja2 templating with Flask for server-side rendering
- **UI Framework**: Bootstrap 5 with dark theme for responsive design
- **JavaScript**: Vanilla JavaScript for file validation, drag-and-drop functionality, and form enhancements
- **Icons**: Font Awesome for consistent iconography
- **Styling**: Custom CSS overlays on Bootstrap for tool-specific styling and hover effects

### Backend Architecture
- **Web Framework**: Flask with Python for lightweight, modular web application structure
- **Request Handling**: RESTful API endpoints for each PDF operation (merge, split, convert, etc.)
- **File Processing**: Modular utility classes for PDF manipulation and file handling
- **Session Management**: Flask sessions with configurable secret key for security
- **Error Handling**: Comprehensive logging and flash message system for user feedback

### File Management System
- **Upload Handling**: Secure file upload with filename sanitization using Werkzeug
- **Temporary Storage**: System temporary directory for processing with automatic cleanup
- **File Validation**: Extension-based filtering and file size limits (50MB maximum)
- **Security**: Secure filename handling and file type validation to prevent malicious uploads

### PDF Processing Engine
- **Core Library**: PyPDF2 for fundamental PDF operations (merge, split, rotate)
- **Document Conversion**: pdf2docx for PDF to Word conversion capabilities
- **Presentation Handling**: python-pptx for PowerPoint format support
- **Archive Creation**: zipfile for packaging multiple output files
- **Memory Management**: BytesIO streams for efficient file processing without disk I/O

### Application Structure
- **Main Application**: app.py contains Flask configuration and route definitions
- **Utility Modules**: Separate classes for PDF operations (PDFTools) and file handling (FileHandler)
- **Template Inheritance**: Base template with consistent navigation and styling across all pages
- **Static Assets**: Organized CSS and JavaScript files for frontend functionality

## External Dependencies

### Python Libraries
- **Flask**: Web framework for application structure and routing
- **PyPDF2**: Core PDF manipulation library for reading, writing, and modifying PDF files
- **pdf2docx**: Specialized library for converting PDF documents to Word format
- **python-pptx**: Library for creating and manipulating PowerPoint presentations
- **Werkzeug**: WSGI utilities for secure file handling and request processing

### Frontend Dependencies
- **Bootstrap 5**: CSS framework delivered via CDN for responsive UI components
- **Font Awesome**: Icon library via CDN for consistent visual elements
- **Bootstrap Agent Dark Theme**: Replit-specific dark theme styling via CDN

### System Dependencies
- **Operating System**: Cross-platform file system operations for upload directory management
- **Temporary File System**: System temp directory for processing intermediate files
- **Logging**: Python's built-in logging system for debugging and monitoring

### Development Dependencies
- **Debug Mode**: Flask debug mode for development with auto-reload capabilities
- **Environment Variables**: Support for production configuration through environment variables