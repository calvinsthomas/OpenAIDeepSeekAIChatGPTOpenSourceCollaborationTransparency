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

