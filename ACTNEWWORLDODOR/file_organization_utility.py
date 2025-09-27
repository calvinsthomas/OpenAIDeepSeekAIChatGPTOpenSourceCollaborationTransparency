#!/usr/bin/env python3
"""
File Organization Utility for ACTNEWWORLDODOR
Addresses issues with file extensions, naming conventions, and flat file alternatives.
"""

import os
import sys
from pathlib import Path

def check_file_extensions(directory="."):
    """Check for files without proper extensions."""
    files_without_ext = []
    
    for root, dirs, files in os.walk(directory):
        # Skip .git directory
        if '.git' in root:
            continue
            
        for file in files:
            if '.' not in file or not file.split('.')[-1]:
                files_without_ext.append(os.path.join(root, file))
    
    return files_without_ext

def suggest_file_extensions(filename):
    """Suggest appropriate file extensions based on content or context."""
    suggestions = {
        'readme': '.md',
        'config': '.xml or .json or .yaml',
        'data': '.csv or .json',
        'script': '.py or .sh or .js',
        'doc': '.md or .rst',
        'text': '.txt',
        'backup': '.bak',
    }
    
    filename_lower = filename.lower()
    for key, extension in suggestions.items():
        if key in filename_lower:
            return extension
    
    return '.txt (default for text files)'

def validate_naming_conventions(directory="."):
    """Check for files that don't follow naming conventions."""
    problematic_files = []
    
    for root, dirs, files in os.walk(directory):
        if '.git' in root:
            continue
            
        # Check directory names for file extensions
        for dir_name in dirs:
            if any(dir_name.endswith(ext) for ext in ['.mp4', '.png', '.jpg', '.jpeg', '.avi', '.mov']):
                problematic_files.append(os.path.join(root, dir_name) + '/ (directory with file extension)')
            
        for file in files:
            # Check for spaces, special characters, or inconsistent casing
            if (' ' in file or 
                any(char in file for char in ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')']) or
                file != file.lower().replace(' ', '_')):
                problematic_files.append(os.path.join(root, file))
    
    return problematic_files

def validate_media_files(directory="."):
    """Check for media files that don't follow naming conventions."""
    media_issues = []
    media_extensions = ['.mp4', '.avi', '.mov', '.wmv', '.png', '.jpg', '.jpeg', '.gif', '.webm']
    
    for root, dirs, files in os.walk(directory):
        if '.git' in root:
            continue
            
        for file in files:
            file_path = os.path.join(root, file)
            file_lower = file.lower()
            
            # Check if it's a media file
            if any(file_lower.endswith(ext) for ext in media_extensions):
                # Check for problematic patterns
                if ('screen recording' in file_lower or
                    'screenshot' in file_lower or
                    ' ' in file or
                    any(char in file for char in ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', "'"])):
                    
                    # Suggest a proper name
                    suggested = suggest_media_filename(file)
                    media_issues.append({
                        'file': file_path,
                        'issue': 'Improper media file naming',
                        'suggested': suggested
                    })
    
    return media_issues

def suggest_media_filename(filename):
    """Suggest proper naming for media files."""
    import re
    from datetime import datetime
    
    # Extract extension
    name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, '')
    
    # Clean up the name
    clean_name = name.lower()
    clean_name = re.sub(r'[^a-z0-9\s\-_]', '', clean_name)  # Remove special chars
    clean_name = re.sub(r'\s+', '_', clean_name)  # Replace spaces with underscores
    
    # Handle common patterns
    if 'screen' in clean_name and 'recording' in clean_name:
        # Extract date if present
        date_match = re.search(r'(\d{4})[-_]?(\d{2})[-_]?(\d{2})', clean_name)
        if date_match:
            date_str = f"{date_match.group(1)}-{date_match.group(2)}-{date_match.group(3)}"
            clean_name = f"screen_recording_{date_str}"
        else:
            clean_name = "screen_recording_demo"
    elif 'screenshot' in clean_name:
        # Extract date if present
        date_match = re.search(r'(\d{4})[-_]?(\d{2})[-_]?(\d{2})', clean_name)
        if date_match:
            date_str = f"{date_match.group(1)}-{date_match.group(2)}-{date_match.group(3)}"
            clean_name = f"screenshot_{date_str}"
        else:
            clean_name = "screenshot_demo"
    
    return f"{clean_name}.{ext.lower()}" if ext else clean_name

def main():
    """Main function to run all validations."""
    print("=== File Organization Validation ===")
    
    # Check for files without extensions
    files_without_ext = check_file_extensions()
    if files_without_ext:
        print(f"\n❌ Files without proper extensions ({len(files_without_ext)}):")
        for file in files_without_ext[:10]:  # Show first 10
            print(f"  {file}")
            suggestion = suggest_file_extensions(os.path.basename(file))
            print(f"    → Suggested: {suggestion}")
        if len(files_without_ext) > 10:
            print(f"  ... and {len(files_without_ext) - 10} more")
    else:
        print("✅ All files have proper extensions")
    
    # Check naming conventions
    problematic_files = validate_naming_conventions()
    if problematic_files:
        print(f"\n❌ Files with naming issues ({len(problematic_files)}):")
        for file in problematic_files[:10]:  # Show first 10
            print(f"  {file}")
        if len(problematic_files) > 10:
            print(f"  ... and {len(problematic_files) - 10} more")
    else:
        print("✅ All files follow naming conventions")
    
    # Check media files specifically
    media_issues = validate_media_files()
    if media_issues:
        print(f"\n❌ Media files with issues ({len(media_issues)}):")
        for issue in media_issues[:10]:  # Show first 10
            print(f"  {issue['file']}")
            print(f"    → {issue['issue']}")
            print(f"    → Suggested: {issue['suggested']}")
        if len(media_issues) > 10:
            print(f"  ... and {len(media_issues) - 10} more")
    else:
        print("✅ All media files follow naming conventions")

if __name__ == "__main__":
    main()

