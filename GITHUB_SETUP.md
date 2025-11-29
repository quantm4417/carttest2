# GitHub Setup Instructions

## Prerequisites

1. **Install Git** (if not already installed):
   - Download from: https://git-scm.com/download/win
   - Install with default settings
   - Restart your terminal after installation

2. **Create a GitHub Account** (if you don't have one):
   - Sign up at: https://github.com/signup

## Quick Setup

### Option 1: Using the PowerShell Script (Easiest)

1. **Install Git** (see above)

2. **Create a new repository on GitHub**:
   - Go to https://github.com/new
   - Repository name: `dampfi-gallery` (or your preferred name)
   - Description: "Premium personal product gallery for dampfi.ch with automated checkout"
   - Choose Public or Private
   - **DO NOT** initialize with README, .gitignore, or license
   - Click "Create repository"

3. **Run the push script**:
   ```powershell
   .\push_to_github.ps1
   ```

4. **If remote is not configured**, add it manually:
   ```powershell
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git branch -M main
   git push -u origin main
   ```

### Option 2: Manual Setup

1. **Initialize git** (if not already done):
   ```powershell
   git init
   ```

2. **Add all files**:
   ```powershell
   git add .
   ```

3. **Create initial commit**:
   ```powershell
   git commit -m "Initial commit: Dampfi Gallery application"
   ```

4. **Create repository on GitHub**:
   - Go to https://github.com/new
   - Create repository (don't initialize with files)

5. **Add remote and push**:
   ```powershell
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git branch -M main
   git push -u origin main
   ```

## What Gets Pushed

The following will be pushed to GitHub:
- ✅ All source code (app/, scripts/)
- ✅ Configuration files (docker-compose.yml, Dockerfile, requirements.txt)
- ✅ Documentation (README.md, QUICKSTART.md)
- ✅ .gitignore (excludes sensitive files)

The following are **NOT** pushed (excluded by .gitignore):
- ❌ `data/` directory (database and uploads)
- ❌ `.env` file (environment variables)
- ❌ `__pycache__/` directories
- ❌ `*.db`, `*.sqlite` files

## After Pushing

1. **Add a repository description** on GitHub
2. **Add topics/tags**: `flask`, `python`, `playwright`, `e-commerce`, `automation`
3. **Consider adding a license** if you want to open source it

## Troubleshooting

### "git is not recognized"
- Install Git from https://git-scm.com/download/win
- Restart your terminal after installation

### "Authentication failed"
- Use a Personal Access Token instead of password
- Generate token: GitHub Settings → Developer settings → Personal access tokens
- Use token as password when pushing

### "Repository not found"
- Check that the repository URL is correct
- Ensure you have write access to the repository



