# PowerShell script to push Dampfi Gallery to GitHub
# Run this after installing Git and creating a GitHub repository

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Pushing Dampfi Gallery to GitHub" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Check if git is available
try {
    $gitVersion = git --version
    Write-Host "Git found: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Git is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Git from: https://git-scm.com/download/win" -ForegroundColor Yellow
    Write-Host "After installation, restart your terminal and run this script again." -ForegroundColor Yellow
    exit 1
}

# Check if already a git repo
if (Test-Path .git) {
    Write-Host "Git repository already initialized" -ForegroundColor Green
} else {
    Write-Host "Initializing git repository..." -ForegroundColor Yellow
    git init
    Write-Host "Git repository initialized" -ForegroundColor Green
}

# Add all files
Write-Host ""
Write-Host "Adding files to git..." -ForegroundColor Yellow
git add .

# Check if there are changes to commit
$status = git status --porcelain
if ($status) {
    Write-Host "Creating initial commit..." -ForegroundColor Yellow
    git commit -m "Initial commit: Dampfi Gallery application
    
    - Flask web application for managing vape liquid products
    - Product gallery with drag-and-drop image upload
    - Metadata scraping from dampfi.ch
    - Automated checkout using Playwright
    - Dark/light theme support
    - User management with 5 user accounts
    - Order history and reporting"
    Write-Host "Commit created successfully" -ForegroundColor Green
} else {
    Write-Host "No changes to commit" -ForegroundColor Yellow
}

# Check for remote
Write-Host ""
$remote = git remote get-url origin 2>$null
if ($remote) {
    Write-Host "Remote already configured: $remote" -ForegroundColor Green
    Write-Host ""
    Write-Host "Pushing to GitHub..." -ForegroundColor Yellow
    git branch -M main
    git push -u origin main
    Write-Host ""
    Write-Host "Successfully pushed to GitHub!" -ForegroundColor Green
} else {
    Write-Host "No remote repository configured" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "To add a remote repository, run:" -ForegroundColor Cyan
    Write-Host "  git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git" -ForegroundColor White
    Write-Host "  git branch -M main" -ForegroundColor White
    Write-Host "  git push -u origin main" -ForegroundColor White
    Write-Host ""
    Write-Host "Or create a new repository on GitHub first:" -ForegroundColor Cyan
    Write-Host "  1. Go to https://github.com/new" -ForegroundColor White
    Write-Host "  2. Create a new repository (don't initialize with README)" -ForegroundColor White
    Write-Host "  3. Copy the repository URL" -ForegroundColor White
    Write-Host "  4. Run the commands above with your repository URL" -ForegroundColor White
}



