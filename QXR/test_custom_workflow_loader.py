#!/usr/bin/env python3
"""
Test suite for QXR Custom Workflow Loader
"""

import unittest
import tempfile
import os
import json
from pathlib import Path
from unittest.mock import patch, MagicMock

from custom_workflow_loader import CustomWorkflowLoader


class TestCustomWorkflowLoader(unittest.TestCase):
    """Test the custom workflow loader functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.mp4_dir = Path(self.temp_dir) / ".mp4"
        self.mp4_dir.mkdir()
        
        self.command_file = self.mp4_dir / "loadmymainquantQXRworkflowcustomnow!"
        
        self.loader = CustomWorkflowLoader(self.temp_dir)
    
    def tearDown(self):
        """Clean up test fixtures"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_loader_initialization(self):
        """Test loader initialization"""
        self.assertEqual(self.loader.base_path, Path(self.temp_dir))
        self.assertEqual(self.loader.mp4_dir, self.mp4_dir)
        self.assertEqual(self.loader.command_file, self.command_file)
    
    def test_command_file_detection(self):
        """Test command file detection"""
        # Initially no command file
        self.assertFalse(self.loader.check_command_file())
        
        # Create command file
        with open(self.command_file, 'w') as f:
            f.write("loadmymainquantQXRworkflowcustomnow!")
        
        # Should now detect command file
        self.assertTrue(self.loader.check_command_file())
    
    def test_command_file_reading(self):
        """Test reading command file content"""
        # No file initially
        content = self.loader.read_command_file()
        self.assertEqual(content, "")
        
        # Create command file with content
        test_command = "loadmymainquantQXRworkflowcustomnow!"
        with open(self.command_file, 'w') as f:
            f.write(test_command)
        
        # Should read correct content
        content = self.loader.read_command_file()
        self.assertEqual(content, test_command)
    
    def test_command_processing(self):
        """Test command processing logic"""
        # Test QXR workflow command
        command = "loadmymainquantQXRworkflowcustomnow!"
        processed = self.loader.process_command(command)
        
        self.assertEqual(processed['action'], 'load_qxr_workflow')
        self.assertTrue(processed['custom'])
        self.assertIn('timestamp', processed)
        
        # Test unknown command
        command = "unknown_command"
        processed = self.loader.process_command(command)
        
        self.assertEqual(processed['action'], 'unknown')
        self.assertEqual(processed['command'], command)
    
    @patch('custom_workflow_loader.run_qxr_main')
    def test_workflow_execution(self, mock_run_qxr_main):
        """Test workflow execution"""
        # Mock successful execution
        mock_run_qxr_main.return_value = True
        
        # Create command file
        with open(self.command_file, 'w') as f:
            f.write("loadmymainquantQXRworkflowcustomnow!")
        
        # Execute workflow
        success = self.loader.execute_custom_workflow()
        
        # Verify execution
        self.assertTrue(success)
        mock_run_qxr_main.assert_called_once()
    
    @patch('custom_workflow_loader.run_qxr_main')
    def test_workflow_execution_failure(self, mock_run_qxr_main):
        """Test workflow execution failure handling"""
        # Mock failed execution
        mock_run_qxr_main.return_value = False
        
        # Create command file
        with open(self.command_file, 'w') as f:
            f.write("loadmymainquantQXRworkflowcustomnow!")
        
        # Execute workflow
        success = self.loader.execute_custom_workflow()
        
        # Verify failure handling
        self.assertFalse(success)
        mock_run_qxr_main.assert_called_once()
    
    @patch('custom_workflow_loader.run_qxr_main')
    def test_execution_logging(self, mock_run_qxr_main):
        """Test execution logging functionality"""
        # Mock successful execution
        mock_run_qxr_main.return_value = True
        
        # Create command file
        with open(self.command_file, 'w') as f:
            f.write("loadmymainquantQXRworkflowcustomnow!")
        
        # Execute workflow
        self.loader.execute_custom_workflow()
        
        # Check if log files were created
        log_dir = Path(self.temp_dir) / "logs" / "custom_workflows"
        self.assertTrue(log_dir.exists())
        
        # Check log file content
        log_files = list(log_dir.glob("*.json"))
        self.assertGreater(len(log_files), 0)
        
        with open(log_files[0], 'r') as f:
            log_data = json.load(f)
        
        self.assertIn('execution_id', log_data)
        self.assertIn('success', log_data)
        self.assertTrue(log_data['success'])
    
    def test_no_command_file_handling(self):
        """Test handling when no command file exists"""
        # Try to execute without command file
        success = self.loader.execute_custom_workflow()
        self.assertFalse(success)


def run_custom_workflow_tests():
    """Run the custom workflow loader test suite"""
    print("🧪 Running Custom Workflow Loader Tests...")
    print("=" * 60)
    
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCustomWorkflowLoader)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print()
    print("=" * 60)
    print("📊 Custom Workflow Loader Test Results:")
    print(f"   Tests run: {result.testsRun}")
    print(f"   Failures: {len(result.failures)}")
    print(f"   Errors: {len(result.errors)}")
    
    success = len(result.failures) == 0 and len(result.errors) == 0
    if success:
        print("🎉 All custom workflow loader tests passed!")
    else:
        print("❌ Some tests failed")
    
    return success


if __name__ == "__main__":
    run_custom_workflow_tests()