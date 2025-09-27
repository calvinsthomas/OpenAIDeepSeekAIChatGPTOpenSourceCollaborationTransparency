#!/bin/bash
# Git LFS File Validation Script
# Usage: ./validate_lfs_file.sh filename.png

FILE="$1"

if [ -z "$FILE" ]; then
    echo "Usage: $0 <filename>"
    echo "Example: $0 screenshot_2025-09-27_demo.png"
    exit 1
fi

if [ ! -f "$FILE" ]; then
    echo "❌ File not found: $FILE"
    exit 1
fi

echo "=== Git LFS File Validation ==="
echo "File: $FILE"

# Check file size
if command -v stat >/dev/null 2>&1; then
    # Try macOS/BSD stat first, then GNU stat
    SIZE=$(stat -f%z "$FILE" 2>/dev/null || stat -c%s "$FILE" 2>/dev/null)
    SIZE_MB=$((SIZE / 1024 / 1024))
    echo "Size: ${SIZE_MB}MB (${SIZE} bytes)"
    
    if [ $SIZE -gt 52428800 ]; then  # 50MB
        echo "⚠️  File is larger than 50MB - GitHub will show warnings"
    fi
    
    if [ $SIZE -gt 104857600 ]; then  # 100MB
        echo "❌ File is larger than 100MB - GitHub will reject it"
    fi
fi

# Check if it matches LFS patterns
echo ""
echo "=== LFS Configuration Check ==="
if git check-attr filter "$FILE" | grep -q "lfs"; then
    echo "✅ File will be handled by Git LFS"
else
    echo "❌ File NOT configured for LFS"
    echo "   This file may be too large for regular Git"
fi

# Check naming convention
echo ""
echo "=== Naming Convention Check ==="
if [[ "$FILE" =~ [[:space:]] ]]; then
    echo "❌ Filename contains spaces"
    SUGGESTED=$(echo "$FILE" | tr ' ' '_' | tr '[:upper:]' '[:lower:]')
    echo "   Suggested: $SUGGESTED"
else
    echo "✅ Filename follows conventions (no spaces)"
fi

# Check for proper screenshot naming
if [[ "$FILE" =~ ^[Ss]creenshot.*\.png$ ]]; then
    if [[ "$FILE" =~ ^screenshot_[0-9]{4}-[0-9]{2}-[0-9]{2}_.*\.png$ ]]; then
        echo "✅ Screenshot follows proper naming pattern"
    else
        echo "❌ Screenshot doesn't follow naming pattern"
        echo "   Expected: screenshot_YYYY-MM-DD_description.png"
        echo "   Example: screenshot_2025-09-27_feature_demo.png"
    fi
fi

echo ""
echo "=== Git LFS Status ==="
git lfs status | head -10

echo ""
echo "=== Next Steps ==="
echo "1. If validation passes, add file: git add '$FILE'"
echo "2. Commit: git commit -m 'Add $(basename "$FILE")'"
echo "3. Push using command line: git push origin <branch>"
echo "4. ⚠️  NEVER upload LFS files via GitHub web interface"