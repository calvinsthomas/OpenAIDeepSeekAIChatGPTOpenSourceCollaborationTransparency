#!/bin/bash
# File Validation Script for ACTNEWWORLDODOR
# This script checks for files without proper extensions and naming conventions

echo "=== File Organization Validation Script ==="
echo "Checking for files without proper extensions..."

# Find files without extensions
files_without_ext=$(find . -type f -not -path "./.git/*" ! -name "*.*" | grep -v "/\." | head -10)

if [ -n "$files_without_ext" ]; then
    echo "❌ Files found without extensions:"
    echo "$files_without_ext"
else
    echo "✅ All files have proper extensions"
fi

echo ""
echo "Checking naming conventions..."

# Check for files with spaces or special characters (excluding allowed ones)
bad_names=$(find . -type f -not -path "./.git/*" -name "* *" -o -name "*!*" -o -name "*@*" | head -10)

if [ -n "$bad_names" ]; then
    echo "❌ Files with poor naming conventions found:"
    echo "$bad_names"
else
    echo "✅ File naming conventions look good"
fi

echo ""
echo "Checking for directories with file extensions..."

# Check for directories that have file extensions (problematic pattern)
bad_dirs=$(find . -type d -not -path "./.git/*" -name "*.mp4" -o -name "*.png" -o -name "*.jpg" -o -name "*.avi" | head -10)

if [ -n "$bad_dirs" ]; then
    echo "❌ Directories with file extensions found:"
    echo "$bad_dirs"
    echo "  → Directories should not have file extensions"
else
    echo "✅ No directories with file extensions found"
fi

echo ""
echo "Checking media file naming..."

# Check for media files with problematic naming patterns
bad_media=$(find . -type f -not -path "./.git/*" \( -name "*Screen Recording*" -o -name "*Screenshot*" \) | head -10)

if [ -n "$bad_media" ]; then
    echo "❌ Media files with poor naming found:"
    echo "$bad_media"
    echo "  → Use descriptive names like 'screen_recording_YYYY-MM-DD_description.mp4'"
else
    echo "✅ Media file naming looks good"
fi

echo ""
echo "=== File Organization Summary ==="
echo "Total files: $(find . -type f -not -path "./.git/*" | wc -l)"
echo "Files with extensions: $(find . -type f -not -path "./.git/*" -name "*.*" | wc -l)"
echo "Documentation files: $(find . -type f -not -path "./.git/*" \( -name "*.md" -o -name "*.rst" -o -name "*.txt" \) | wc -l)"
echo "Data files: $(find . -type f -not -path "./.git/*" \( -name "*.csv" -o -name "*.xml" -o -name "*.xlsx" -o -name "*.json" \) | wc -l)"