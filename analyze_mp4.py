#!/usr/bin/env python3
import os

def analyze_repository():
    print("=== Analyzing .mp4 File Issues ===")
    
    mp4_files = []
    problematic_files = []
    
    for root, dirs, files in os.walk("."):
        if '.git' in root:
            continue
        for file in files:
            file_path = os.path.join(root, file)
            if file.endswith('.mp4'):
                mp4_files.append(file_path)
                
                # Check for problematic naming
                if (not file.replace('.mp4', '') or  # Just .mp4 extension
                    ' ' in file or  # Spaces
                    any(char in file for char in ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', "'"])):
                    problematic_files.append(file_path)
    
    print(f"Found {len(mp4_files)} .mp4 files:")
    for f in mp4_files:
        print(f"  {f}")
    
    print(f"\nProblematic .mp4 files ({len(problematic_files)}):")
    for f in problematic_files:
        print(f"  ❌ {f}")
        # Suggest a fix
        basename = os.path.basename(f)
        fixed_name = basename.lower().replace(' ', '_').replace("'", '').replace('(', '').replace(')', '').replace('@', 'at_').replace('!', '')
        if fixed_name == '.mp4':
            fixed_name = 'untitled_video.mp4'
        print(f"     → Suggested: {fixed_name}")
    
    return mp4_files, problematic_files

if __name__ == "__main__":
    analyze_repository()
