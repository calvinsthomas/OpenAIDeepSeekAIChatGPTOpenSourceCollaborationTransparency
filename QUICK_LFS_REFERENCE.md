# Quick Git LFS Reference Card

## 🚨 Critical Requirement
**PNG files MUST be pushed using Git command line with Git LFS installed!**

## 📋 Quick Commands

### First Time Setup
```bash
git lfs install
./scripts/setup_git_lfs.sh
```

### Adding PNG Files
```bash
# 1. Validate file first
./scripts/validate_lfs_file.sh your_file.png

# 2. Add normally (LFS handles automatically)
git add your_file.png

# 3. Commit
git commit -m "Add screenshot"

# 4. Push via command line (REQUIRED!)
git push origin main
```

### For "Screenshot 2025-09-27 130131.png"
```bash
# If file exists - rename first
mv "Screenshot 2025-09-27 130131.png" "screenshot_2025-09-27_130131.png"

# Then follow standard workflow above
git add screenshot_2025-09-27_130131.png
git commit -m "Add screenshot_2025-09-27_130131.png"
git push origin main
```

## ❌ Never Use
- GitHub web interface upload
- Drag and drop
- Some GUI clients

## ✅ Always Use
- Git command line
- Terminal/PowerShell
- IDEs with proper LFS support

## 📚 Full Documentation
- `GIT_LFS_SETUP_GUIDE.md` - Complete guide
- `SCREENSHOT_LFS_INSTRUCTIONS.md` - Specific file instructions
- `LFS_SOLUTION_SUMMARY.md` - Implementation summary