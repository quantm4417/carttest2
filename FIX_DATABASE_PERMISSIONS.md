# Fix Database Permissions Error

If you're getting `sqlite3.OperationalError: attempt to write a readonly database`, follow these steps:

## Quick Fix

Run the permissions fix script:

```bash
chmod +x fix_permissions.sh
./fix_permissions.sh
```

## Manual Fix

If the script doesn't work, fix permissions manually:

```bash
# Navigate to your project directory
cd ~/test/new/carttest2

# Fix data directory permissions
chmod -R 755 data/

# Fix database file permissions
chmod 644 data/database.db

# Fix uploads directory
chmod -R 755 data/uploads/
```

## If You Don't Own the Files

If you get "Permission denied" errors, you may need to change ownership:

```bash
# Change ownership to your user
sudo chown -R $USER:$USER data/

# Then set permissions
chmod -R 755 data/
chmod 644 data/database.db
```

## Verify Permissions

Check the permissions:

```bash
ls -la data/
ls -la data/database.db
```

You should see:
- `data/` directory: `drwxr-xr-x` (755)
- `database.db` file: `-rw-r--r--` (644)

## After Fixing

Restart your Flask application:

```bash
python3 run.py
```

The database should now be writable!

