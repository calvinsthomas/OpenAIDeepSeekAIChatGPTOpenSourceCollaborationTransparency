#!/bin/bash
# Git LFS Setup and Verification Script
# Run this script to ensure Git LFS is properly configured

echo "=== Git LFS Setup and Verification ==="

# Check if Git LFS is installed
if ! command -v git-lfs >/dev/null 2>&1; then
    echo "❌ Git LFS is not installed"
    echo ""
    echo "Installation instructions:"
    echo "  Ubuntu/Debian: sudo apt install git-lfs"
    echo "  macOS:         brew install git-lfs"
    echo "  Windows:       Download from https://git-lfs.github.io/"
    exit 1
fi

echo "✅ Git LFS is installed"
git lfs version

# Initialize Git LFS in the repository
echo ""
echo "=== Initializing Git LFS ==="
git lfs install

# Verify LFS configuration
echo ""
echo "=== Current LFS Tracking Configuration ==="
echo "Files tracked by LFS:"
git lfs track

echo ""
echo "=== Current LFS Status ==="
git lfs status

echo ""
echo "=== LFS Files in Repository ==="
LFS_FILES=$(git lfs ls-files | wc -l)
echo "Number of LFS files: $LFS_FILES"

if [ $LFS_FILES -gt 0 ]; then
    echo "Recent LFS files:"
    git lfs ls-files | head -5
    if [ $LFS_FILES -gt 5 ]; then
        echo "  ... and $((LFS_FILES - 5)) more"
    fi
fi

echo ""
echo "=== Repository Health Check ==="

# Check for improperly named files that should be in LFS
echo "Checking for files that might need LFS..."
LARGE_FILES=$(find . -type f -size +10M -not -path "./.git/*" 2>/dev/null)
if [ -n "$LARGE_FILES" ]; then
    echo "⚠️  Large files found (>10MB):"
    echo "$LARGE_FILES" | head -5
    echo "   Consider adding these to Git LFS if they're binary files"
else
    echo "✅ No large files found outside of LFS"
fi

# Check for poorly named screenshot files
POOR_SCREENSHOTS=$(find . -name "*Screenshot*" -o -name "*Screen Shot*" 2>/dev/null | grep -v ".git")
if [ -n "$POOR_SCREENSHOTS" ]; then
    echo ""
    echo "⚠️  Screenshots with poor naming found:"
    echo "$POOR_SCREENSHOTS" | head -3
    echo "   Consider renaming to: screenshot_YYYY-MM-DD_description.png"
fi

echo ""
echo "=== Git LFS Setup Complete ==="
echo ""
echo "Quick reference for working with LFS files:"
echo "1. Add file:    git add your_file.png"
echo "2. Commit:      git commit -m 'Add screenshot'"
echo "3. Push:        git push origin main"
echo "4. Validate:    ./scripts/validate_lfs_file.sh your_file.png"
echo ""
echo "⚠️  Important: Always push LFS files using git command line!"
echo "   Never use GitHub web interface for LFS files."