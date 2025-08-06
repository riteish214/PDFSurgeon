import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
import os
import logging
# Flask url_for is not available in this context

class QRGenerator:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def generate_qr_code(self, access_code, output_path, base_url=None):
        """Generate QR code for shared file access"""
        try:
            # Create the full URL for accessing the shared file
            if base_url:
                data = f"{base_url}/shared/{access_code}"
            else:
                # Use relative URL that will work with any domain
                data = f"/shared/{access_code}"
            
            # Create QR code with custom styling
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            
            qr.add_data(data)
            qr.make(fit=True)
            
            # Create styled QR code image
            img = qr.make_image(
                image_factory=StyledPilImage,
                module_drawer=RoundedModuleDrawer(),
                fill_color="#FF7F11",  # Orange color to match theme
                back_color="#000000"   # Black background
            )
            
            # Ensure output directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Save the QR code
            img.save(output_path)
            
            return output_path
        
        except Exception as e:
            self.logger.error(f"Error generating QR code: {str(e)}")
            raise Exception(f"Failed to generate QR code: {str(e)}")
    
    def generate_simple_qr_code(self, data, output_path):
        """Generate simple QR code for any data"""
        try:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            
            qr.add_data(data)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Ensure output directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            img.save(output_path)
            
            return output_path
        
        except Exception as e:
            self.logger.error(f"Error generating simple QR code: {str(e)}")
            raise Exception(f"Failed to generate QR code: {str(e)}")
    
    def generate_qr_with_logo(self, data, output_path, logo_path=None):
        """Generate QR code with optional logo in center"""
        try:
            from PIL import Image, ImageDraw
            
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,  # Higher error correction for logo
                box_size=10,
                border=4,
            )
            
            qr.add_data(data)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            
            if logo_path and os.path.exists(logo_path):
                # Add logo to center
                logo = Image.open(logo_path)
                
                # Calculate logo size (10% of QR code)
                qr_width, qr_height = img.size
                logo_size = min(qr_width, qr_height) // 10
                logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
                
                # Calculate position to center the logo
                logo_pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
                
                img.paste(logo, logo_pos)
            
            # Ensure output directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            img.save(output_path)
            
            return output_path
        
        except Exception as e:
            self.logger.error(f"Error generating QR code with logo: {str(e)}")
            raise Exception(f"Failed to generate QR code with logo: {str(e)}")