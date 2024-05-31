# Convert Images to PDF

Convert an image directory to a single PDF. Includes image shrinking and adding watermarks.

## Sample Run

```
 ./run_converter.sh 
Enter the directory containing images (default './images'): ./images
Enter the output PDF file name (default 'images.pdf'): images.png
Enter the quality ('w' for web size, 'o' for original size, default 'o'): w
Enter the watermark text or image file path (leave empty for no watermark): logo.png
Enter the watermark position ('center', 'top-left', 'top-right', 'bottom-left', 'bottom-right', default 'bottom-right'): center
 ```

## Setup

### First Time

For first time run of any scripts use

```
chmod +x ./run_converter.sh
```

### Setup Enviorment

```
python3 -m venv .venv
. .venv/bin/activate
```