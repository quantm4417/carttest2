# Quick Start Guide

## Prerequisites
- Python 3.11+ OR Docker & Docker Compose
- Internet connection (for scraping dampfi.ch)

## Option 1: Docker (Recommended)

```bash
# 1. Initialize database
python scripts/init_db.py

# 2. Start application
docker-compose up -d

# 3. Open browser
# http://localhost:5000
```

## Option 2: Direct Python

```bash
# 1. Install dependencies
pip install -r requirements.txt
playwright install chromium

# 2. Initialize database
python scripts/init_db.py

# 3. Run application
python run.py
# or
python -m flask run
```

## First Steps After Starting

1. **Configure Users (1-5)**
   - Navigate to User Setup (or it will prompt you during checkout)
   - Enter dampfi.ch email and password for each user you want to use

2. **Add Products**
   - Go to "Product Management"
   - Click "Add New Product"
   - Enter product URL from dampfi.ch (e.g., `https://www.dampfi.ch/elfbar-elfliq-cola-10ml-liquid-nik-salz.html`)
   - Enter product name
   - Upload product image (drag & drop)
   - Click "Save Product"
   - Click "Scrape Metadata" to fetch current price and options

3. **Use Gallery**
   - Go to "Gallery"
   - Select products with quantities and options
   - Click "Review Selection"
   - Click "Proceed to Checkout"
   - Select user (1-5)
   - Review and confirm order

## Troubleshooting

- **Database errors**: Delete `data/database.db` and run `python scripts/init_db.py` again
- **Image upload fails**: Check file size (max 10MB) and format (WebP/JPEG)
- **Scraping fails**: Check internet connection and verify dampfi.ch is accessible
- **Playwright errors**: Run `playwright install chromium` to install browsers

## Environment Variables

Create `.env` file (copy from `.env.example`):
- `SECRET_KEY`: Flask secret key (change in production!)
- `DATABASE_PATH`: Path to SQLite database
- `UPLOAD_FOLDER`: Path to upload directory



