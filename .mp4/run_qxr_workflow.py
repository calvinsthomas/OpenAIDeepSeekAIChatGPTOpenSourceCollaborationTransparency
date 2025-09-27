#!/usr/bin/env python3
"""
QXR Workflow Runner for .mp4 directory
Direct execution script for the custom QXR workflow
"""

import sys
import os
from pathlib import Path

# Add QXR directory to path
qxr_dir = Path(__file__).parent.parent / "QXR"
sys.path.insert(0, str(qxr_dir))

try:
    from custom_workflow_loader import CustomWorkflowLoader
    
    def main():
        """Run the custom QXR workflow from .mp4 directory"""
        print("🎬 .MP4 QXR WORKFLOW RUNNER")
        print("=" * 50)
        print("📁 Running from .mp4 directory")
        print()
        
        # Initialize loader with correct base path
        base_path = Path(__file__).parent.parent
        loader = CustomWorkflowLoader(str(base_path))
        
        # Execute the workflow
        if loader.check_command_file():
            success = loader.execute_custom_workflow()
            if success:
                print()
                print("✅ Workflow execution completed successfully!")
                print("📄 Check the generated files in /tmp/")
                print("📋 Execution logs saved in logs/custom_workflows/")
            else:
                print("❌ Workflow execution failed")
            return success
        else:
            print("❌ Command file not found")
            print(f"Expected: {loader.command_file}")
            return False
    
    if __name__ == "__main__":
        success = main()
        sys.exit(0 if success else 1)
        
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please ensure QXR modules are properly installed")
    sys.exit(1)