import os
import logging
from flask import Flask, render_template, request, send_file, flash, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
from utils.pdf_tools import PDFTools
from utils.file_handler import FileHandler
import tempfile
import shutil

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")

# Configuration
UPLOAD_FOLDER = 'uploads'
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB (increased from 50MB)
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'ppt', 'pptx'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize utilities
pdf_tools = PDFTools()
file_handler = FileHandler(UPLOAD_FOLDER, ALLOWED_EXTENSIONS)

@app.route('/')
def index():
    """Home page with overview of all tools"""
    return render_template('index.html')

@app.route('/merge')
def merge():
    """PDF merge tool page"""
    return render_template('merge.html')

@app.route('/split')
def split():
    """PDF split tool page"""
    return render_template('split.html')

@app.route('/convert')
def convert():
    """File conversion tool page"""
    return render_template('convert.html')

@app.route('/compress')
def compress():
    """PDF compression tool page"""
    return render_template('compress.html')

@app.route('/rotate')
def rotate():
    """PDF rotation tool page"""
    return render_template('rotate.html')

@app.route('/secure')
def secure():
    """PDF security tool page"""
    return render_template('secure.html')

@app.route('/api/merge', methods=['POST'])
def api_merge():
    """Merge multiple PDF files"""
    try:
        files = request.files.getlist('files')
        if len(files) < 2:
            flash('Please select at least 2 PDF files to merge.', 'error')
            return redirect(url_for('merge'))

        # Validate and save uploaded files
        temp_files = []
        for file in files:
            if not file_handler.validate_file(file, ['pdf']):
                flash(f'Invalid file: {file.filename}. Only PDF files are allowed.', 'error')
                return redirect(url_for('merge'))
            
            temp_path = file_handler.save_temp_file(file)
            temp_files.append(temp_path)

        # Merge PDFs
        output_path = pdf_tools.merge_pdfs(temp_files)
        
        # Clean up temp files
        for temp_file in temp_files:
            file_handler.cleanup_file(temp_file)

        return send_file(output_path, as_attachment=True, download_name='merged.pdf')

    except Exception as e:
        logging.error(f"Error merging PDFs: {str(e)}")
        flash(f'Error merging PDFs: {str(e)}', 'error')
        return redirect(url_for('merge'))

@app.route('/api/split', methods=['POST'])
def api_split():
    """Split PDF into individual pages"""
    try:
        file = request.files['file']
        if not file_handler.validate_file(file, ['pdf']):
            flash('Please select a valid PDF file.', 'error')
            return redirect(url_for('split'))

        temp_path = file_handler.save_temp_file(file)
        
        # Split PDF
        output_dir = pdf_tools.split_pdf(temp_path)
        
        # Create zip file with all pages
        zip_path = file_handler.create_zip(output_dir, 'split_pages.zip')
        
        # Clean up
        file_handler.cleanup_file(temp_path)
        shutil.rmtree(output_dir)

        return send_file(zip_path, as_attachment=True, download_name='split_pages.zip')

    except Exception as e:
        logging.error(f"Error splitting PDF: {str(e)}")
        flash(f'Error splitting PDF: {str(e)}', 'error')
        return redirect(url_for('split'))

@app.route('/api/convert', methods=['POST'])
def api_convert():
    """Convert between different file formats"""
    try:
        file = request.files['file']
        conversion_type = request.form.get('conversion_type')
        
        if not file_handler.validate_file(file):
            flash('Please select a valid file.', 'error')
            return redirect(url_for('convert'))

        temp_path = file_handler.save_temp_file(file)
        
        # Perform conversion based on type
        if conversion_type == 'pdf_to_word':
            output_path = pdf_tools.pdf_to_word(temp_path)
            download_name = 'converted.docx'
        elif conversion_type == 'pdf_to_ppt':
            output_path = pdf_tools.pdf_to_ppt(temp_path)
            download_name = 'converted.pptx'
        elif conversion_type == 'word_to_pdf':
            output_path = pdf_tools.word_to_pdf(temp_path)
            download_name = 'converted.pdf'
        elif conversion_type == 'ppt_to_pdf':
            output_path = pdf_tools.ppt_to_pdf(temp_path)
            download_name = 'converted.pdf'
        else:
            flash('Invalid conversion type selected.', 'error')
            return redirect(url_for('convert'))

        # Clean up
        file_handler.cleanup_file(temp_path)

        return send_file(output_path, as_attachment=True, download_name=download_name)

    except Exception as e:
        logging.error(f"Error converting file: {str(e)}")
        flash(f'Error converting file: {str(e)}', 'error')
        return redirect(url_for('convert'))

@app.route('/api/compress', methods=['POST'])
def api_compress():
    """Compress PDF file"""
    try:
        file = request.files['file']
        if not file_handler.validate_file(file, ['pdf']):
            flash('Please select a valid PDF file.', 'error')
            return redirect(url_for('compress'))

        temp_path = file_handler.save_temp_file(file)
        
        # Compress PDF
        output_path = pdf_tools.compress_pdf(temp_path)
        
        # Clean up
        file_handler.cleanup_file(temp_path)

        return send_file(output_path, as_attachment=True, download_name='compressed.pdf')

    except Exception as e:
        logging.error(f"Error compressing PDF: {str(e)}")
        flash(f'Error compressing PDF: {str(e)}', 'error')
        return redirect(url_for('compress'))

@app.route('/api/rotate', methods=['POST'])
def api_rotate():
    """Rotate PDF pages"""
    try:
        file = request.files['file']
        rotation = int(request.form.get('rotation', 90))
        pages = request.form.get('pages', 'all')
        
        if not file_handler.validate_file(file, ['pdf']):
            flash('Please select a valid PDF file.', 'error')
            return redirect(url_for('rotate'))

        temp_path = file_handler.save_temp_file(file)
        
        # Rotate PDF
        output_path = pdf_tools.rotate_pdf(temp_path, rotation, pages)
        
        # Clean up
        file_handler.cleanup_file(temp_path)

        return send_file(output_path, as_attachment=True, download_name='rotated.pdf')

    except Exception as e:
        logging.error(f"Error rotating PDF: {str(e)}")
        flash(f'Error rotating PDF: {str(e)}', 'error')
        return redirect(url_for('rotate'))

@app.route('/api/secure', methods=['POST'])
def api_secure():
    """Add password protection to PDF"""
    try:
        file = request.files['file']
        password = request.form.get('password')
        
        if not file_handler.validate_file(file, ['pdf']):
            flash('Please select a valid PDF file.', 'error')
            return redirect(url_for('secure'))

        if not password:
            flash('Please provide a password.', 'error')
            return redirect(url_for('secure'))

        temp_path = file_handler.save_temp_file(file)
        
        # Add password protection
        output_path = pdf_tools.encrypt_pdf(temp_path, password)
        
        # Clean up
        file_handler.cleanup_file(temp_path)

        return send_file(output_path, as_attachment=True, download_name='protected.pdf')

    except Exception as e:
        logging.error(f"Error securing PDF: {str(e)}")
        flash(f'Error securing PDF: {str(e)}', 'error')
        return redirect(url_for('secure'))

@app.errorhandler(413)
def too_large(e):
    flash('File too large. Maximum file size is 100MB.', 'error')
    return redirect(request.referrer or url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
