# Large File Handling Guidelines

## Overview

This repository implements a comprehensive approach to handling large files to ensure optimal GitHub performance and user experience.

## File Size Strategy

### 🚫 Excluded Files (via .gitignore)
Large media files that exceed GitHub's display limits are excluded from version control:

- **Video files**: `*.mp4`, `*.avi`, `*.mov`, `*.mkv`, `*.wmv`, `*.flv`, `*.webm`, `*.m4v`, `*.3gp`
- **Large audio files**: `*.wav`, `*.flac`, `*.aiff`, `*.m4a`, `*.wma`
- **Large image formats**: `*.psd`, `*.ai`, `*.eps`, `*.indd`, `*.raw`, `*.cr2`, `*.nef`, `*.orf`, `*.sr2`

### 📦 Git LFS Files (via .gitattributes)
Essential project files that are large but necessary for documentation and collaboration:

- **Documentation images**: `*.png`, `*.jpg`, `*.jpeg`, `*.gif`, `*.bmp`, `*.tiff`, `*.webp`
- **Office documents**: `*.docx`, `*.xlsx`, `*.pptx`
- **Archives**: `*.pdf`, `*.zip`, `*.7z`, `*.tar.gz`, `*.rar`

## GitHub File Size Limits

GitHub has the following file size restrictions:
- **Warning**: Files larger than 50 MB
- **Block**: Files larger than 100 MB
- **Display**: Files over ~5-10 MB may show "Sorry about that, but we can't show files that are this big right now"

## Best Practices

### For Developers
1. **Use external storage** for large media files (cloud storage, CDN)
2. **Compress images** before committing when possible
3. **Link to external resources** in documentation rather than embedding large files
4. **Use Git LFS** for essential large files that must be version controlled

### For Large Media Files
If you need to include large video files or media:

1. **Upload to external platform** (YouTube, Vimeo, cloud storage)
2. **Create a markdown link** in the documentation
3. **Add thumbnails or screenshots** as smaller preview images

Example:
```markdown
## Demo Video
[📹 View Demo Recording](https://youtu.be/your-video-id)
![Demo Preview](./screenshots/demo-preview.png)
```

## Migration Notes

If you encounter the "files that are this big" error on GitHub:
1. Large media files have been moved to `.gitignore`
2. Essential images and documents are now handled via Git LFS
3. Documentation has been updated with external links where appropriate

## Git LFS Setup

To work with Git LFS files in this repository:

```bash
# Install Git LFS
git lfs install

# Clone with LFS files
git lfs clone <repository-url>

# Or pull LFS files in existing clone
git lfs pull
```

## Contact

For questions about file handling in this repository, please refer to the main project documentation or open an issue.