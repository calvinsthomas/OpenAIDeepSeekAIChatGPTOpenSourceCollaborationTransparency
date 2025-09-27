# Git LFS Setup and Usage Guide

## Overview

This repository uses Git LFS (Large File Storage) to efficiently handle large binary files including images, documents, and archives. Files configured for Git LFS **must be pushed using the Git command line** with Git LFS properly installed.

## Quick Start

### 1. Install Git LFS

```bash
# On Ubuntu/Debian
sudo apt install git-lfs

# On macOS
brew install git-lfs

# On Windows
# Download from: https://git-lfs.github.io/
```

### 2. Initialize Git LFS in Your Repository

```bash
# Navigate to your repository
cd /path/to/repository

# Initialize Git LFS (one-time setup)
git lfs install
```

### 3. Verify LFS Configuration

```bash
# Check which file types are tracked by LFS
git lfs track

# Check LFS status
git lfs status
```

## Files Tracked by Git LFS

According to our `.gitattributes` configuration, the following files are handled by Git LFS:

### Image Files
- `*.png` - Screenshots, diagrams, documentation images
- `*.jpg`, `*.jpeg` - Photos, compressed images  
- `*.gif` - Animated images
- `*.bmp`, `*.tiff`, `*.webp` - Other image formats

### Document Files
- `*.pdf` - PDF documents
- `*.docx` - Word documents
- `*.xlsx` - Excel spreadsheets
- `*.pptx` - PowerPoint presentations

### Archive Files
- `*.zip` - ZIP archives
- `*.7z` - 7-Zip archives
- `*.tar.gz` - Compressed tar archives
- `*.rar` - RAR archives

## Working with LFS Files

### Adding New LFS Files

```bash
# Add your file normally
git add your_file.png

# Commit (LFS handles the large file automatically)
git commit -m "Add new screenshot"

# Push to remote (MUST use git command line)
git push origin your-branch
```

### Important: Always Use Git Command Line

⚠️ **Critical Requirement**: Files configured for Git LFS **MUST be pushed using the Git command line**. Web interfaces and some GUI tools may not handle LFS files correctly.

```bash
# ✅ Correct way to push LFS files
git push origin main

# ❌ Avoid using web interface for LFS files
# GitHub web interface upload may fail for LFS-tracked files
```

### Cloning Repository with LFS Files

```bash
# Option 1: Clone with LFS files
git lfs clone https://github.com/user/repo.git

# Option 2: Clone normally then pull LFS files
git clone https://github.com/user/repo.git
cd repo
git lfs pull
```

## File Naming Requirements

Before adding files to LFS, ensure they follow our naming conventions:

### ✅ Correct Screenshot Names
- `screenshot_2025-09-27_feature_demo.png`
- `api_error_screenshot_2025-09-27.png`
- `ui_mockup_dashboard.png`

### ❌ Incorrect Screenshot Names
- `Screenshot 2025-09-27 130131.png` (spaces, generic)
- `Screen Shot.png` (spaces, no description)
- `IMG_001.png` (generic, no context)

## Troubleshooting Common Issues

### Issue: "This file is tracked by LFS but not present"

```bash
# Solution: Pull LFS files
git lfs pull
```

### Issue: "Failed to push some refs" with LFS files

```bash
# Check LFS status
git lfs status

# Ensure LFS is initialized
git lfs install

# Try pushing again
git push origin main
```

### Issue: Large file rejected by GitHub

```bash
# Check if file should be in LFS
file_size=$(stat -f%z "your_file.png")
echo "File size: $((file_size / 1024 / 1024)) MB"

# If >50MB and not in LFS, it should be added to .gitattributes
```

## Verification Scripts

### Check LFS Status

```bash
#!/bin/bash
# Check overall LFS status
echo "=== Git LFS Status ==="
git lfs status

echo -e "\n=== Tracked Patterns ==="
git lfs track

echo -e "\n=== LFS Objects in Repository ==="
git lfs ls-files
```

### Validate File Before Adding

```bash
#!/bin/bash
# Usage: ./validate_lfs_file.sh filename.png

FILE="$1"
if [ ! -f "$FILE" ]; then
    echo "File not found: $FILE"
    exit 1
fi

# Check file size
SIZE=$(stat -f%z "$FILE" 2>/dev/null || stat -c%s "$FILE")
SIZE_MB=$((SIZE / 1024 / 1024))

echo "File: $FILE"
echo "Size: ${SIZE_MB}MB"

# Check if it matches LFS patterns
if git check-attr filter "$FILE" | grep -q "lfs"; then
    echo "✅ File will be handled by LFS"
else
    echo "❌ File NOT configured for LFS"
fi

# Check naming convention
if [[ "$FILE" =~ [[:space:]] ]]; then
    echo "❌ Filename contains spaces - consider renaming"
    SUGGESTED=$(echo "$FILE" | tr ' ' '_' | tr '[:upper:]' '[:lower:]')
    echo "   Suggested: $SUGGESTED"
fi
```

## Best Practices

1. **Always verify LFS is working**: Use `git lfs status` before committing large files
2. **Use descriptive filenames**: Follow naming conventions before adding to LFS
3. **Push from command line**: Never rely on web interfaces for LFS files
4. **Regular maintenance**: Periodically run `git lfs prune` to clean up old LFS objects
5. **Team coordination**: Ensure all team members have Git LFS installed

## Example: Adding Screenshot to LFS

```bash
# 1. Create properly named screenshot
# Bad:  Screenshot 2025-09-27 130131.png
# Good: screenshot_2025-09-27_lfs_demo.png

# 2. Add to git
git add screenshot_2025-09-27_lfs_demo.png

# 3. Verify it will use LFS
git lfs status

# 4. Commit
git commit -m "Add LFS demo screenshot"

# 5. Push using command line (REQUIRED)
git push origin main
```

## Support

For issues with Git LFS in this repository:
1. Check this guide first
2. Verify your Git LFS installation: `git lfs version`
3. Review the repository's `LARGE_FILE_HANDLING.md`
4. Open an issue with LFS status output: `git lfs status`