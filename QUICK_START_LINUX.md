# Quick Start - Native Linux

## One-Command Setup

```bash
chmod +x setup_linux.sh && ./setup_linux.sh
```

## After Setup

1. **Set SECRET_KEY in .env:**
   ```bash
   openssl rand -hex 32  # Copy this
   nano .env  # Paste as SECRET_KEY value
   ```

2. **Start the app:**
   ```bash
   ./start.sh
   ```

3. **Open browser:**
   - http://localhost:5000

4. **Configure users:**
   - Go to User Setup
   - Enter dampfi.ch credentials for users 1-5

5. **Add products:**
   - Go to Product Management
   - Add product URLs
   - Upload images
   - Scrape metadata

That's it! 🎉

