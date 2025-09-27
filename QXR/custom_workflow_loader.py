#!/usr/bin/env python3
"""
QXR Custom Workflow Loader
Monitors and processes custom workflow commands from file system triggers
"""

import os
import sys
import time
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional

# Add current directory to path for imports
current_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(current_dir))

from qxr_main import main as run_qxr_main


class CustomWorkflowLoader:
    """Handles custom workflow loading and execution based on file triggers"""
    
    def __init__(self, base_path: Optional[str] = None):
        self.base_path = Path(base_path) if base_path else Path(__file__).parent.parent
        self.mp4_dir = self.base_path / ".mp4"
        self.command_file = self.mp4_dir / "loadmymainquantQXRworkflowcustomnow!"
        
    def check_command_file(self) -> bool:
        """Check if the custom workflow command file exists"""
        return self.command_file.exists()
    
    def read_command_file(self) -> str:
        """Read the content of the command file"""
        if self.check_command_file():
            try:
                with open(self.command_file, 'r', encoding='utf-8') as f:
                    return f.read().strip()
            except Exception as e:
                print(f"❌ Error reading command file: {e}")
                return ""
        return ""
    
    def process_command(self, command: str) -> Dict[str, Any]:
        """Process the custom workflow command"""
        print("🔍 Processing custom workflow command...")
        print(f"📄 Command: {command}")
        
        # Parse the command
        if "loadmymainquantQXRworkflow" in command:
            return {
                'action': 'load_qxr_workflow',
                'custom': 'customnow' in command,
                'timestamp': datetime.now().isoformat(),
                'source': str(self.command_file)
            }
        
        return {
            'action': 'unknown',
            'command': command,
            'timestamp': datetime.now().isoformat()
        }
    
    def execute_custom_workflow(self) -> bool:
        """Execute the custom QXR workflow"""
        print("🚀 CUSTOM QXR WORKFLOW LOADER")
        print("=" * 60)
        print(f"📅 Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📁 Trigger source: {self.command_file}")
        print()
        
        # Read and process command
        command = self.read_command_file()
        if not command:
            print("❌ No command found or unable to read command file")
            return False
        
        processed_command = self.process_command(command)
        print(f"✅ Command processed: {processed_command['action']}")
        
        if processed_command['action'] == 'load_qxr_workflow':
            print("🎯 Executing main QXR workflow...")
            print()
            
            # Create execution log
            log_entry = {
                'execution_id': f"custom_{int(time.time())}",
                'trigger_source': str(self.command_file),
                'command': command,
                'processed_command': processed_command,
                'started_at': datetime.now().isoformat()
            }
            
            try:
                # Execute the main QXR workflow
                success = run_qxr_main()
                
                log_entry['completed_at'] = datetime.now().isoformat()
                log_entry['success'] = success
                
                # Save execution log
                self.save_execution_log(log_entry)
                
                if success:
                    print()
                    print("🎉 CUSTOM WORKFLOW EXECUTION COMPLETE!")
                    print(f"📋 Execution log saved")
                    return True
                else:
                    print("❌ Workflow execution failed")
                    return False
                    
            except Exception as e:
                log_entry['completed_at'] = datetime.now().isoformat()
                log_entry['success'] = False
                log_entry['error'] = str(e)
                self.save_execution_log(log_entry)
                
                print(f"❌ Error executing workflow: {e}")
                return False
        else:
            print(f"❌ Unknown command action: {processed_command['action']}")
            return False
    
    def save_execution_log(self, log_entry: Dict[str, Any]) -> str:
        """Save execution log to file"""
        log_dir = self.base_path / "logs" / "custom_workflows"
        log_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = log_dir / f"custom_workflow_execution_{timestamp}.json"
        
        try:
            with open(log_file, 'w', encoding='utf-8') as f:
                json.dump(log_entry, f, indent=2, default=str)
            print(f"📋 Execution log: {log_file}")
            return str(log_file)
        except Exception as e:
            print(f"⚠️ Warning: Could not save execution log: {e}")
            return ""
    
    def monitor_command_file(self, interval: int = 5) -> None:
        """Monitor the command file for changes (for daemon mode)"""
        print("👁️ Monitoring custom workflow commands...")
        print(f"📁 Watching: {self.command_file}")
        print("Press Ctrl+C to stop monitoring")
        
        last_modified = 0
        
        try:
            while True:
                if self.check_command_file():
                    current_modified = self.command_file.stat().st_mtime
                    
                    if current_modified > last_modified:
                        print(f"\n🔔 Command file updated at {datetime.now()}")
                        self.execute_custom_workflow()
                        last_modified = current_modified
                
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n🛑 Monitoring stopped by user")


def main():
    """Main function for custom workflow loader"""
    loader = CustomWorkflowLoader()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--monitor":
            loader.monitor_command_file()
            return
        elif sys.argv[1] == "--help":
            print("""
QXR Custom Workflow Loader

Usage:
  python custom_workflow_loader.py          - Execute workflow if command file exists
  python custom_workflow_loader.py --monitor - Monitor command file for changes
  python custom_workflow_loader.py --help   - Show this help

Command file location: .mp4/loadmymainquantQXRworkflowcustomnow!
""")
            return
    
    # Check if command file exists and execute
    if loader.check_command_file():
        success = loader.execute_custom_workflow()
        sys.exit(0 if success else 1)
    else:
        print("❌ No custom workflow command file found")
        print(f"Expected location: {loader.command_file}")
        sys.exit(1)


if __name__ == "__main__":
    main()