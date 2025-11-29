# Fix Permission Error

If you're getting a `PermissionError: [Errno 13] Permission denied: '/app'` error, it means your `.env` file has Docker paths.

## Quick Fix

Edit your `.env` file and remove or comment out the Docker paths:

```bash
nano .env
```

Remove or comment these lines:
```
# DATABASE_PATH=/app/data/database.db
# UPLOAD_FOLDER=/app/data/uploads
```

Or set them to relative paths:
```
DATABASE_PATH=./data/database.db
UPLOAD_FOLDER=./data/uploads
```

The application will use relative paths by default (in the `data/` directory of your project).

## After Fixing

Restart the application:
```bash
python3 run.py
```

