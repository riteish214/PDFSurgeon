import os
import tempfile
import zipfile
from PyPDF2 import PdfReader, PdfWriter
import pdfplumber
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import logging

class PDFProcessor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def merge_pdfs(self, pdf_files):
        """Merge multiple PDF files into one"""
        try:
            writer = PdfWriter()
            
            for pdf_file in pdf_files:
                reader = PdfReader(pdf_file)
                for page in reader.pages:
                    writer.add_page(page)
            
            # Create output file
            output_path = os.path.join(tempfile.gettempdir(), 'merged.pdf')
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
            
            return output_path
        
        except Exception as e:
            self.logger.error(f"Error merging PDFs: {str(e)}")
            raise Exception(f"Failed to merge PDFs: {str(e)}")
    
    def split_pdf(self, pdf_path):
        """Split PDF into individual pages and return as zip"""
        try:
            reader = PdfReader(pdf_path)
            output_dir = tempfile.mkdtemp()
            
            # Split into individual pages
            for page_num, page in enumerate(reader.pages, 1):
                writer = PdfWriter()
                writer.add_page(page)
                
                page_path = os.path.join(output_dir, f'page_{page_num:03d}.pdf')
                with open(page_path, 'wb') as output_file:
                    writer.write(output_file)
            
            # Create zip file
            zip_path = os.path.join(tempfile.gettempdir(), 'split_pages.zip')
            with zipfile.ZipFile(zip_path, 'w') as zip_file:
                for file_name in os.listdir(output_dir):
                    file_path = os.path.join(output_dir, file_name)
                    zip_file.write(file_path, file_name)
            
            return zip_path
        
        except Exception as e:
            self.logger.error(f"Error splitting PDF: {str(e)}")
            raise Exception(f"Failed to split PDF: {str(e)}")
    
    def compress_pdf(self, pdf_path):
        """Compress PDF by reducing image quality"""
        try:
            reader = PdfReader(pdf_path)
            writer = PdfWriter()
            
            for page in reader.pages:
                page.compress_content_streams()
                writer.add_page(page)
            
            output_path = os.path.join(tempfile.gettempdir(), 'compressed.pdf')
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
            
            return output_path
        
        except Exception as e:
            self.logger.error(f"Error compressing PDF: {str(e)}")
            raise Exception(f"Failed to compress PDF: {str(e)}")
    
    def encrypt_pdf(self, pdf_path, password):
        """Add password protection to PDF"""
        try:
            reader = PdfReader(pdf_path)
            writer = PdfWriter()
            
            for page in reader.pages:
                writer.add_page(page)
            
            writer.encrypt(password)
            
            output_path = os.path.join(tempfile.gettempdir(), 'encrypted.pdf')
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
            
            return output_path
        
        except Exception as e:
            self.logger.error(f"Error encrypting PDF: {str(e)}")
            raise Exception(f"Failed to encrypt PDF: {str(e)}")
    
    def decrypt_pdf(self, pdf_path, password):
        """Remove password protection from PDF"""
        try:
            reader = PdfReader(pdf_path)
            
            if reader.is_encrypted:
                reader.decrypt(password)
            
            writer = PdfWriter()
            for page in reader.pages:
                writer.add_page(page)
            
            output_path = os.path.join(tempfile.gettempdir(), 'decrypted.pdf')
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
            
            return output_path
        
        except Exception as e:
            self.logger.error(f"Error decrypting PDF: {str(e)}")
            raise Exception(f"Failed to decrypt PDF: {str(e)}")
    
    def extract_text(self, pdf_path):
        """Extract text from PDF using pdfplumber"""
        try:
            text_content = ""
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    text_content += page.extract_text() or ""
                    text_content += "\n\n"
            
            return text_content.strip()
        
        except Exception as e:
            self.logger.error(f"Error extracting text from PDF: {str(e)}")
            raise Exception(f"Failed to extract text from PDF: {str(e)}")
    
    def pdf_to_csv(self, pdf_path):
        """Extract tables from PDF and convert to CSV"""
        try:
            import pandas as pd
            
            tables = []
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_tables = page.extract_tables()
                    if page_tables:
                        tables.extend(page_tables)
            
            if not tables:
                raise Exception("No tables found in PDF")
            
            # Convert first table to CSV
            df = pd.DataFrame(tables[0][1:], columns=tables[0][0])
            output_path = os.path.join(tempfile.gettempdir(), 'extracted_table.csv')
            df.to_csv(output_path, index=False)
            
            return output_path
        
        except Exception as e:
            self.logger.error(f"Error converting PDF to CSV: {str(e)}")
            raise Exception(f"Failed to convert PDF to CSV: {str(e)}")