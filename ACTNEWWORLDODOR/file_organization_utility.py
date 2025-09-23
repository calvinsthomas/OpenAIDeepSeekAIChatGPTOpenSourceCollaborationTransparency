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
            
        for file in files:
            # Check for spaces, special characters, or inconsistent casing
            if (' ' in file or 
                any(char in file for char in ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')']) or
                file != file.lower().replace(' ', '_')):
                problematic_files.append(os.path.join(root, file))
    
    return problematic_files

def main():
    """Main function to run file organization checks."""
    print("=== ACTNEWWORLDODOR File Organization Utility ===")
    print("Checking for file organization issues...\n")
    
    # Check for files without extensions
    files_no_ext = check_file_extensions()
    if files_no_ext:
        print("❌ Files without proper extensions found:")
        for file in files_no_ext[:10]:  # Show first 10
            suggested_ext = suggest_file_extensions(os.path.basename(file))
            print(f"  {file} -> Suggested: {suggested_ext}")
        if len(files_no_ext) > 10:
            print(f"  ... and {len(files_no_ext) - 10} more files")
    else:
        print("✅ All files have proper extensions")
    
    print()
    
    # Check naming conventions
    bad_names = validate_naming_conventions()
    if bad_names:
        print("❌ Files with naming convention issues:")
        for file in bad_names[:10]:  # Show first 10
            print(f"  {file}")
        if len(bad_names) > 10:
            print(f"  ... and {len(bad_names) - 10} more files")
    else:
        print("✅ File naming conventions are good")
    
    print()
    print("=== Recommendations ===")
    print("1. Add proper file extensions (.csv, .xml, .xlsx, .txt, .md)")
    print("2. Use underscore_separated_names for files")
    print("3. Avoid special characters and spaces in filenames")
    print("4. Add shebang lines to executable scripts")
    print("5. Set executable permissions for scripts")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())