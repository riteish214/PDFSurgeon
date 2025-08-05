"""
File handling utilities for secure upload and processing
"""
import os
import tempfile
import logging
import zipfile
import shutil
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage

logger = logging.getLogger(__name__)

class FileHandler:
    """
    Handles file uploads, validation, and cleanup
    """
    
    def __init__(self, upload_folder, allowed_extensions):
        self.upload_folder = upload_folder
        self.allowed_extensions = allowed_extensions
        self.temp_dir = tempfile.gettempdir()
        
        # Ensure upload folder exists
        os.makedirs(upload_folder, exist_ok=True)
    
    def validate_file(self, file, allowed_types=None):
        """
        Validate uploaded file
        
        Args:
            file (FileStorage): Uploaded file object
            allowed_types (list): Specific file types to allow
            
        Returns:
            bool: True if file is valid
        """
        if not file or file.filename == '':
            return False
        
        # Use specific allowed types if provided, otherwise use default
        extensions = allowed_types or self.allowed_extensions
        
        # Check file extension
        if not self._allowed_file(file.filename, extensions):
            logger.warning(f"Invalid file type: {file.filename}")
            return False
        
        # Check if file has content
        file.seek(0, os.SEEK_END)
        size = file.tell()
        file.seek(0)  # Reset file pointer
        
        if size == 0:
            logger.warning(f"Empty file: {file.filename}")
            return False
        
        # File size validation (50MB max)
        max_size = 50 * 1024 * 1024  # 50MB
        if size > max_size:
            logger.warning(f"File too large: {file.filename} ({size} bytes)")
            return False
        
        return True
    
    def _allowed_file(self, filename, allowed_extensions):
        """
        Check if file extension is allowed
        
        Args:
            filename (str): Name of the file
            allowed_extensions (set): Set of allowed extensions
            
        Returns:
            bool: True if extension is allowed
        """
        return ('.' in filename and 
                filename.rsplit('.', 1)[1].lower() in allowed_extensions)
    
    def save_temp_file(self, file):
        """
        Save uploaded file to temporary location
        
        Args:
            file (FileStorage): Uploaded file object
            
        Returns:
            str: Path to saved temporary file
        """
        try:
            # Generate secure filename
            filename = secure_filename(file.filename)
            
            # Create unique temporary file
            temp_file = tempfile.NamedTemporaryFile(
                delete=False,
                suffix=f"_{filename}",
                dir=self.temp_dir
            )
            
            # Save file content
            file.save(temp_file.name)
            temp_file.close()
            
            logger.info(f"Saved temporary file: {temp_file.name}")
            return temp_file.name
            
        except Exception as e:
            logger.error(f"Error saving temporary file: {str(e)}")
            raise Exception(f"Failed to save file: {str(e)}")
    
    def save_upload_file(self, file):
        """
        Save uploaded file to upload folder
        
        Args:
            file (FileStorage): Uploaded file object
            
        Returns:
            str: Path to saved file
        """
        try:
            filename = secure_filename(file.filename)
            
            # Add timestamp to prevent conflicts
            import time
            timestamp = str(int(time.time()))
            name, ext = os.path.splitext(filename)
            unique_filename = f"{name}_{timestamp}{ext}"
            
            filepath = os.path.join(self.upload_folder, unique_filename)
            file.save(filepath)
            
            logger.info(f"Saved upload file: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Error saving upload file: {str(e)}")
            raise Exception(f"Failed to save file: {str(e)}")
    
    def create_zip(self, directory, zip_name):
        """
        Create ZIP file from directory contents
        
        Args:
            directory (str): Path to directory to zip
            zip_name (str): Name of the ZIP file
            
        Returns:
            str: Path to created ZIP file
        """
        try:
            zip_path = os.path.join(self.temp_dir, zip_name)
            
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(directory):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, directory)
                        zipf.write(file_path, arcname)
            
            logger.info(f"Created ZIP file: {zip_path}")
            return zip_path
            
        except Exception as e:
            logger.error(f"Error creating ZIP file: {str(e)}")
            raise Exception(f"Failed to create ZIP file: {str(e)}")
    
    def cleanup_file(self, filepath):
        """
        Delete a file safely
        
        Args:
            filepath (str): Path to file to delete
        """
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
                logger.info(f"Cleaned up file: {filepath}")
        except Exception as e:
            logger.warning(f"Error cleaning up file {filepath}: {str(e)}")
    
    def cleanup_directory(self, directory):
        """
        Delete a directory and all its contents
        
        Args:
            directory (str): Path to directory to delete
        """
        try:
            if os.path.exists(directory):
                shutil.rmtree(directory)
                logger.info(f"Cleaned up directory: {directory}")
        except Exception as e:
            logger.warning(f"Error cleaning up directory {directory}: {str(e)}")
    
    def get_file_info(self, filepath):
        """
        Get information about a file
        
        Args:
            filepath (str): Path to the file
            
        Returns:
            dict: File information including size, type, etc.
        """
        try:
            if not os.path.exists(filepath):
                return None
            
            stat = os.stat(filepath)
            filename = os.path.basename(filepath)
            name, ext = os.path.splitext(filename)
            
            return {
                'name': filename,
                'size': stat.st_size,
                'size_mb': round(stat.st_size / (1024 * 1024), 2),
                'extension': ext.lower().lstrip('.'),
                'modified': stat.st_mtime,
                'path': filepath
            }
            
        except Exception as e:
            logger.error(f"Error getting file info: {str(e)}")
            return None
    
    def cleanup_old_files(self, max_age_hours=24):
        """
        Clean up old temporary files
        
        Args:
            max_age_hours (int): Maximum age of files in hours
        """
        try:
            import time
            current_time = time.time()
            max_age_seconds = max_age_hours * 3600
            
            cleaned_count = 0
            
            # Clean upload folder
            for filename in os.listdir(self.upload_folder):
                filepath = os.path.join(self.upload_folder, filename)
                if os.path.isfile(filepath):
                    file_age = current_time - os.path.getmtime(filepath)
                    if file_age > max_age_seconds:
                        self.cleanup_file(filepath)
                        cleaned_count += 1
            
            # Clean temp directory (only files created by our app)
            for filename in os.listdir(self.temp_dir):
                if any(keyword in filename.lower() for keyword in ['merged', 'split', 'compressed', 'rotated', 'protected', 'converted']):
                    filepath = os.path.join(self.temp_dir, filename)
                    if os.path.isfile(filepath):
                        file_age = current_time - os.path.getmtime(filepath)
                        if file_age > max_age_seconds:
                            self.cleanup_file(filepath)
                            cleaned_count += 1
            
            if cleaned_count > 0:
                logger.info(f"Cleaned up {cleaned_count} old files")
                
        except Exception as e:
            logger.error(f"Error cleaning up old files: {str(e)}")
