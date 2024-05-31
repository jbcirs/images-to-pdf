from PIL import Image, ImageDraw, ImageFont
import os
from PyPDF2 import PdfMerger
import pillow_heif

# Define size variables
WEB_SIZE = 800  # Max dimension for web size
ORIGINAL_SIZE = None  # Use None to keep the original size

def convert_image_to_rgb(image_path):
    img = Image.open(image_path)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    return img

def resize_image(image, max_size):
    """Resize image maintaining aspect ratio."""
    if max_size:
        image.thumbnail((max_size, max_size), Image.LANCZOS)
    return image

def add_text_watermark(image, watermark_text, position):
    """Add a text watermark to the image."""
    drawable = ImageDraw.Draw(image)
    font_size = max(15, image.size[0] // 20)
    
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()
    
    # Calculate text size
    bbox = drawable.textbbox((0, 0), watermark_text, font=font)
    textwidth = bbox[2] - bbox[0]
    textheight = bbox[3] - bbox[1]
    
    # Determine position
    if position == 'center':
        x = (image.size[0] - textwidth) / 2
        y = (image.size[1] - textheight) / 2
    elif position == 'top-left':
        x, y = 10, 10
    elif position == 'top-right':
        x = image.size[0] - textwidth - 10
        y = 10
    elif position == 'bottom-left':
        x = 10
        y = image.size[1] - textheight - 10
    else:  # bottom-right
        x = image.size[0] - textwidth - 10
        y = image.size[1] - textheight - 10
    
    drawable.text((x, y), watermark_text, font=font, fill=(255, 255, 255, 128))
    return image

def add_image_watermark(image, watermark_image_path, position):
    """Add an image watermark to the image."""
    watermark = Image.open(watermark_image_path).convert("RGBA")
    watermark = resize_image(watermark, min(image.size) // 5)
    watermark_width, watermark_height = watermark.size
    
    if position == 'center':
        x = (image.size[0] - watermark_width) // 2
        y = (image.size[1] - watermark_height) // 2
    elif position == 'top-left':
        x, y = 10, 10
    elif position == 'top-right':
        x = image.size[0] - watermark_width - 10
        y = 10
    elif position == 'bottom-left':
        x = 10
        y = image.size[1] - watermark_height - 10
    else:  # bottom-right
        x = image.size[0] - watermark_width - 10
        y = image.size[1] - watermark_height - 10
    
    image.paste(watermark, (x, y), watermark)
    return image

def images_to_pdf(directory, output_pdf, quality, watermark, position):
    # Supported image formats
    supported_formats = ['jpg', 'jpeg', 'heic', 'gif', 'png']
    
    # Collect all supported image files in the directory
    image_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.split('.')[-1].lower() in supported_formats]
    
    if not image_files:
        print("No supported image files found in the directory.")
        return
    
    # Sort files to maintain a consistent order in the PDF
    image_files.sort()

    images = []
    for file in image_files:
        img = convert_image_to_rgb(file)
        
        # Resize image based on the quality setting
        if quality == 'w':
            img = resize_image(img, WEB_SIZE)  # Resize for web use
        elif quality == 'o':
            img = resize_image(img, ORIGINAL_SIZE)  # Keep the original size
        
        # Add watermark if provided
        if watermark:
            if os.path.isfile(watermark):
                img = add_image_watermark(img, watermark, position)
            else:
                img = add_text_watermark(img, watermark, position)
        
        images.append(img)

    # Save the images as a PDF
    if images:
        images[0].save(output_pdf, save_all=True, append_images=images[1:])
        print(f"PDF created successfully: {output_pdf}")
    else:
        print("No valid images to convert to PDF.")

if __name__ == "__main__":
    directory = input("Enter the directory containing images (default './images'): ") or './images'
    output_pdf = input("Enter the output PDF file name (default 'images.pdf'): ") or 'images.pdf'
    quality = input("Enter the quality ('w' for web size, 'o' for original size, default 'o'): ").lower() or 'o'
    watermark = input("Enter the watermark text or image file path (leave empty for no watermark): ")
    position = input("Enter the watermark position ('center', 'top-left', 'top-right', 'bottom-left', 'bottom-right', default 'bottom-right'): ") or 'bottom-right'
    
    if quality not in ['w', 'o']:
        print("Invalid quality option. Please choose 'w' or 'o'.")
    else:
        images_to_pdf(directory, output_pdf, quality, watermark, position)
