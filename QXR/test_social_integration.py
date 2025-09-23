#!/usr/bin/env python3
"""
QXR Social Media Integration Tests
Comprehensive test suite for the social media posting functionality
"""

import sys
import os
import json
import tempfile
import shutil
from datetime import datetime
import unittest
from unittest.mock import patch, MagicMock

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import modules to test
from social_media_engine import SocialMediaEngine, PostContent, SocialPlatform
from notebook_to_social import NotebookProcessor


class TestSocialMediaEngine(unittest.TestCase):
    """Test the social media engine functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.engine = SocialMediaEngine("TESTFIRM")
        self.sample_research_data = {
            'signals': 45,
            'opportunities': 8,
            'signal_strength': 1.247,
            'price_range': [3420, 3580],
            'max_liquidity': 12500000,
            'strategy': 'ETH Statistical Arbitrage',
            'timeframe': '24h'
        }
    
    def test_engine_initialization(self):
        """Test proper engine initialization"""
        self.assertEqual(self.engine.firm_id, "TESTFIRM")
        self.assertIsNotNone(self.engine.session_key)
        self.assertTrue(self.engine.session_key.startswith("🌐"))
        self.assertIn("TESTFIRM", self.engine.session_key)
    
    def test_authentication_session(self):
        """Test COMBSEC authentication"""
        session_key = self.engine.authenticate_session()
        self.assertIsNotNone(session_key)
        self.assertEqual(os.environ.get('QXR_SOCIAL_COMBSEC_KEY'), session_key)
    
    def test_research_post_generation(self):
        """Test generating post content from research data"""
        post = self.engine.generate_research_post(self.sample_research_data)
        
        self.assertIsInstance(post, PostContent)
        self.assertIn("QXR ETH Liquidity Research", post.title)
        self.assertIn("45", post.content)  # signals
        self.assertIn("8", post.content)   # opportunities
        self.assertIn("1.247", post.content)  # signal strength
        self.assertIn("#ETH", post.hashtags)
        self.assertIn("#QXR", post.hashtags)
        self.assertEqual(post.combsec_key, self.engine.session_key)
    
    def test_platform_formatting(self):
        """Test platform-specific content formatting"""
        post = self.engine.generate_research_post(self.sample_research_data)
        
        # Test LinkedIn formatting (longer content allowed)
        linkedin_content = self.engine.format_for_platform(post, 'linkedin')
        self.assertIn(post.title, linkedin_content)
        self.assertIn("#ETH", linkedin_content)
        self.assertLessEqual(len(linkedin_content), 3000)
        
        # Test Twitter formatting (shorter content)
        twitter_content = self.engine.format_for_platform(post, 'twitter')
        self.assertIn(post.title, twitter_content)
        self.assertLessEqual(len(twitter_content), 280)
        
        # Test GitHub formatting (no hashtags)
        github_content = self.engine.format_for_platform(post, 'github')
        self.assertIn(post.title, github_content)
        # GitHub doesn't support hashtags in this implementation
    
    def test_manual_post_preparation(self):
        """Test preparing posts for manual publishing"""
        target_platforms = ['linkedin', 'twitter', 'github']
        posts = self.engine.prepare_manual_post(self.sample_research_data, target_platforms)
        
        self.assertEqual(len(posts), 3)
        self.assertIn('linkedin', posts)
        self.assertIn('twitter', posts)
        self.assertIn('github', posts)
        
        for platform, content in posts.items():
            self.assertIsInstance(content, str)
            self.assertGreater(len(content), 0)
    
    def test_one_push_manual_prepare(self):
        """Test the main one-push preparation functionality"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Override the output directory for testing
            with patch.object(self.engine, 'save_posts_for_manual_publishing') as mock_save:
                mock_save.return_value = os.path.join(temp_dir, "test_posts.md")
                
                master_file, posts = self.engine.one_push_manual_prepare(
                    self.sample_research_data, 
                    ['linkedin', 'twitter']
                )
                
                self.assertIsInstance(master_file, str)
                self.assertIsInstance(posts, dict)
                self.assertEqual(len(posts), 2)
                mock_save.assert_called_once()
    
    def test_invalid_platform_handling(self):
        """Test handling of invalid platform names"""
        with self.assertRaises(ValueError):
            post = self.engine.generate_research_post(self.sample_research_data)
            self.engine.format_for_platform(post, 'invalid_platform')
    
    def test_posting_instructions(self):
        """Test generation of posting instructions"""
        instructions = self.engine.get_posting_instructions()
        self.assertIsInstance(instructions, str)
        self.assertIn("AUTHENTICATION", instructions)
        self.assertIn("COMBSEC", instructions)
        self.assertIn("LinkedIn", instructions)
        self.assertIn("Twitter", instructions)


class TestNotebookProcessor(unittest.TestCase):
    """Test the notebook processing functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.notebook_path = os.path.join(self.temp_dir, "test_notebook.ipynb")
        
        # Create a sample notebook for testing
        self.sample_notebook = {
            "cells": [
                {
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": ["# Test Notebook"]
                },
                {
                    "cell_type": "code",
                    "metadata": {},
                    "source": ["# Sample calculation\nsignals = 45\nopportunities = 8"],
                    "outputs": [
                        {
                            "output_type": "stream",
                            "name": "stdout",
                            "text": ["Total signals: 45\nRecent opportunities: 8\nAvg signal strength: 1.247"]
                        }
                    ]
                }
            ],
            "metadata": {"kernelspec": {"name": "python3"}},
            "nbformat": 4,
            "nbformat_minor": 4
        }
        
        with open(self.notebook_path, 'w') as f:
            json.dump(self.sample_notebook, f)
        
        self.processor = NotebookProcessor(self.notebook_path)
    
    def tearDown(self):
        """Clean up test fixtures"""
        shutil.rmtree(self.temp_dir)
    
    def test_processor_initialization(self):
        """Test processor initialization"""
        self.assertEqual(self.processor.notebook_path, self.notebook_path)
        self.assertIsNone(self.processor.notebook)
    
    def test_notebook_loading(self):
        """Test loading notebook from file"""
        success = self.processor.load_notebook()
        self.assertTrue(success)
        self.assertIsNotNone(self.processor.notebook)
        self.assertIn('cells', self.processor.notebook)
    
    def test_research_metrics_extraction(self):
        """Test extracting research metrics from notebook"""
        metrics = self.processor.extract_research_metrics()
        
        self.assertIsInstance(metrics, dict)
        self.assertIn('notebook_name', metrics)
        self.assertIn('analysis_type', metrics)
        self.assertIn('signals', metrics)
        self.assertIn('opportunities', metrics)
        
        # Should extract values from the sample notebook
        self.assertGreater(metrics['signals'], 0)
        self.assertGreater(metrics['opportunities'], 0)
    
    def test_output_text_parsing(self):
        """Test parsing output text for metrics"""
        sample_text = "Total signals: 45\nRecent opportunities: 8\nAvg signal strength: 1.247"
        metrics = self.processor._parse_output_text(sample_text)
        
        self.assertEqual(metrics['signals'], 45)
        self.assertEqual(metrics['opportunities'], 8)
        self.assertEqual(metrics['signal_strength'], 1.247)
    
    def test_source_code_parsing(self):
        """Test parsing source code for variables"""
        sample_code = "signals = 45\nopportunities = 8\nsignal_strength = 1.247"
        metrics = self.processor._parse_source_code(sample_code)
        
        # Basic parsing should find signal-related variables
        self.assertIsInstance(metrics, dict)
    
    def test_invalid_notebook_handling(self):
        """Test handling of invalid notebook files"""
        invalid_path = "/nonexistent/notebook.ipynb"
        processor = NotebookProcessor(invalid_path)
        
        success = processor.load_notebook()
        self.assertFalse(success)
        
        # Should still return default metrics
        metrics = processor.extract_research_metrics()
        self.assertIsInstance(metrics, dict)
        # For invalid notebooks, we should get empty dict or defaults


class TestIntegration(unittest.TestCase):
    """Test the full integration workflow"""
    
    def setUp(self):
        """Set up integration test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        
        # Create sample research data
        self.research_data = {
            'signals': 42,
            'opportunities': 7,
            'signal_strength': 1.156,
            'price_range': [3400, 3600],
            'max_liquidity': 11000000,
            'strategy': 'Test Strategy',
            'timeframe': '12h'
        }
    
    def tearDown(self):
        """Clean up integration test fixtures"""
        shutil.rmtree(self.temp_dir)
    
    def test_end_to_end_workflow(self):
        """Test the complete end-to-end workflow"""
        engine = SocialMediaEngine("TESTINTEGRATION")
        
        # Test the one-push manual workflow
        master_file, posts = engine.one_push_manual_prepare(
            self.research_data,
            target_platforms=['linkedin', 'twitter']
        )
        
        # Verify outputs
        self.assertIsInstance(master_file, str)
        self.assertIsInstance(posts, dict)
        self.assertEqual(len(posts), 2)
        
        # Check post content quality
        for platform, content in posts.items():
            self.assertIn("ETH Liquidity Research", content)
            self.assertIn("42", content)  # signals
            self.assertIn("7", content)   # opportunities
            self.assertIn("🔐 Verified with", content)  # COMBSEC reference
    
    def test_combsec_integration(self):
        """Test COMBSEC key integration throughout workflow"""
        engine = SocialMediaEngine("TESTSECURITY")
        
        # Verify COMBSEC key is properly generated and used
        self.assertTrue(engine.session_key.startswith("🌐"))
        self.assertIn("TESTSECURITY", engine.session_key)
        
        # Test authentication
        session_key = engine.authenticate_session()
        self.assertEqual(session_key, engine.session_key)
        
        # Verify key is included in posts
        post = engine.generate_research_post(self.research_data)
        self.assertEqual(post.combsec_key, session_key)
        
        # Verify key appears in formatted content
        linkedin_content = engine.format_for_platform(post, 'linkedin')
        self.assertIn(session_key[:20], linkedin_content)


def run_comprehensive_tests():
    """Run all tests with detailed output"""
    print("🌐 QXR Social Media Integration - Comprehensive Test Suite")
    print("=" * 70)
    
    # Create test suite
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTest(unittest.makeSuite(TestSocialMediaEngine))
    suite.addTest(unittest.makeSuite(TestNotebookProcessor))
    suite.addTest(unittest.makeSuite(TestIntegration))
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    result = runner.run(suite)
    
    # Summary
    print("\n" + "=" * 70)
    print(f"📊 Test Results Summary:")
    print(f"   Tests run: {result.testsRun}")
    print(f"   Failures: {len(result.failures)}")
    print(f"   Errors: {len(result.errors)}")
    print(f"   Skipped: {len(result.skipped) if hasattr(result, 'skipped') else 0}")
    
    if result.failures:
        print(f"\n❌ Failures:")
        for test, traceback in result.failures:
            error_lines = traceback.split('\n')
            error_msg = next((line for line in reversed(error_lines) if line.strip()), "Unknown error")
            print(f"   {test}: {error_msg}")
    
    if result.errors:
        print(f"\n💥 Errors:")
        for test, traceback in result.errors:
            error_lines = traceback.split('\n')
            error_msg = next((line for line in reversed(error_lines) if line.strip()), "Unknown error")
            print(f"   {test}: {error_msg}")
    
    if len(result.failures) + len(result.errors) == 0:
        print("🎉 All tests passed! QXR Social Media Integration is ready for deployment.")
        return True
    else:
        print("💥 Some tests failed. Please review and fix issues.")
        return False


if __name__ == "__main__":
    # Run comprehensive tests
    success = run_comprehensive_tests()
    sys.exit(0 if success else 1)