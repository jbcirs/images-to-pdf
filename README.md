# Convert Images to PDF

Convert an image directory to a single PDF.

## Sample Run

```
 ./run_converter.sh 
 Enter the directory containing images: ./images
 PDF created successfully: filename.pdf
 Enter the quality ('web' for web size, 'original' for original size): web
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