# Dampfi Gallery

A premium personal product gallery application for managing and ordering vape liquids from dampfi.ch.

## Features

- **Product Gallery**: View your favorite vape liquids with high-quality images
- **Product Management**: Add, edit, and manage products with drag-and-drop image upload
- **Metadata Scraping**: Automatically fetch current prices, stock status, and options from dampfi.ch
- **Smart Selection**: Select products with quantities and options before checkout
- **Automated Checkout**: Automated checkout process using Playwright
- **Order History**: View recent orders and reporting
- **Dark/Light Theme**: Built-in theme switcher
- **User Management**: Support for 5 user accounts with individual credentials

## Requirements

- Python 3.11+
- Docker and Docker Compose (recommended)
- Or run directly with Python

## Quick Start

### Installation (One-Time Setup)

After cloning the repository, run:

```bash
chmod +x install_setup.sh
./install_setup.sh
```

This will:
- Install all system dependencies
- Create Python virtual environment
- Install Python packages
- Install Playwright browsers
- Create `.env` file with auto-generated SECRET_KEY
- Initialize database
- Set up all directories

### Start the Application

```bash
./start.sh
```

The application will be available at: **http://localhost:5000**

### First Steps

1. **Configure users:**
   - Navigate to User Setup (via gallery or directly)
   - Configure dampfi.ch credentials for users 1-5

2. **Add products:**
   - Go to Product Management
   - Add product URLs from dampfi.ch
   - Upload images and scrape metadata

### Using Docker (Alternative)

1. **Build and start:**
   ```bash
   docker-compose build
   docker-compose up -d
   ```

2. **Seed users:**
   ```bash
   docker-compose exec flask_app python scripts/seed_users.py
   ```

See [LINUX_SETUP.md](LINUX_SETUP.md) for detailed native Linux setup instructions.

## Project Structure

```
dampfi/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── config.py             # Configuration
│   ├── database.py           # Database utilities
│   ├── models.py             # Database models
│   ├── routes/               # Flask routes
│   │   ├── views.py         # Web UI routes
│   │   └── api.py           # API endpoints
│   ├── services/             # Business logic
│   │   ├── scraper.py       # Metadata scraping
│   │   └── automation.py    # Playwright checkout
│   ├── static/              # Static assets
│   │   ├── css/            # Stylesheets
│   │   └── js/             # JavaScript
│   ├── templates/           # Jinja2 templates
│   └── utils/              # Utilities
├── scripts/                 # Setup scripts
│   ├── init_db.py          # Database initialization
│   └── seed_users.py       # User seeding
├── data/                   # Data directory (created on setup)
│   ├── database.db         # SQLite database
│   └── uploads/            # Product images
├── docker-compose.yml      # Docker Compose config
├── Dockerfile              # Docker image
├── requirements.txt       # Python dependencies
└── setup.sh               # First-time setup script
```

## Usage

### Adding Products

1. Go to **Product Management**
2. Click **Add New Product**
3. Enter the product URL from dampfi.ch
4. Enter product name
5. Upload an image (drag & drop or click to browse)
6. Click **Save Product**
7. Click **Scrape Metadata** to fetch current price and options

### Selecting Products for Checkout

1. Go to **Gallery**
2. For each product:
   - Select an option (nicotine strength)
   - Choose quantity (1-5)
   - Click **Add to Selection**
3. Click **Review Selection** to see summary
4. Click **Proceed to Checkout**

### Checkout Process

1. On the checkout review page:
   - Select user (1-5)
   - Review selected items and total price
   - View recent orders
2. Click **Confirm & Place Order**
3. The system will:
   - Login to dampfi.ch
   - Add all items to cart
   - Complete checkout with saved credentials
   - Show confirmation

### User Setup

1. Navigate to User Setup (or from checkout if credentials missing)
2. Enter dampfi.ch email and password
3. Credentials are stored securely in the database

## API Endpoints

- `GET /` - Gallery view
- `GET /product-management` - Product management UI
- `GET /checkout/review` - Checkout review page
- `GET /user/setup` - User credentials setup
- `GET /api/products` - List all products
- `POST /api/products` - Create product
- `PUT /api/products/<id>` - Update product
- `DELETE /api/products/<id>` - Delete product
- `POST /api/products/<id>/scrape` - Scrape metadata
- `POST /api/products/<id>/upload` - Upload product image
- `POST /api/user/<id>/credentials` - Save user credentials
- `POST /api/checkout/confirm` - Execute checkout
- `GET /api/user/<id>/orders` - Get user orders
- `GET /api/logs?debug=true` - Get logs (debug mode)

## Database Schema

### Users
- id, username, email, dampfi_email, dampfi_password, created_at

### Products
- id, product_url, name, price, stock_status, options (JSON), image_path, created_at, updated_at

### Orders
- id, user_id, timestamp, total_price, items (JSON), status, confirmation_data (JSON)

### Logs
- id, timestamp, level, message, context (JSON)

## Configuration

Create a `.env` file (copy from `.env.example`):

```env
FLASK_APP=app
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
DATABASE_PATH=/app/data/database.db
UPLOAD_FOLDER=/app/data/uploads
MAX_UPLOAD_SIZE=10485760
```

## Docker Volumes

- `db_data`: SQLite database persistence
- `image_uploads`: Product image uploads

## Troubleshooting

### Playwright Issues
- Ensure Playwright browsers are installed: `playwright install chromium`
- In Docker, browsers are installed automatically

### Database Issues
- Database is created automatically on first run
- To reset: delete `data/database.db` and run `python scripts/init_db.py`

### Image Upload Issues
- Check file size (max 10MB)
- Supported formats: WebP, JPEG, JPG
- Ensure upload directory has write permissions

## Development

```bash
# Install development dependencies
pip install -r requirements.txt

# Run in development mode
export FLASK_ENV=development
python -m flask run --debug

# Run database migrations (if needed)
python scripts/init_db.py
```

## License

Private project for personal use.



