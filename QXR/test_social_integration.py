#!/usr/bin/env python3
"""
QXR Social Media Integration Tests
Comprehensive test suite for the social media posting functionality
Enhanced with Notion page generation and Backtest Sim Landing Page tests
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
from notion_page_generator import NotionPageGenerator, BacktestResult


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


class TestNotionPageGenerator(unittest.TestCase):
    """Test the Notion page generation functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.generator = NotionPageGenerator("TESTFIRM")
        self.sample_research_data = {
            'signals': 45,
            'opportunities': 8,
            'signal_strength': 1.247,
            'price_range': [3420, 3580],
            'max_liquidity': 12500000,
            'strategy': 'ETH Statistical Arbitrage',
            'timeframe': '24h'
        }
    
    def test_generator_initialization(self):
        """Test proper generator initialization"""
        self.assertEqual(self.generator.firm_id, "TESTFIRM")
        self.assertIsNotNone(self.generator.session_key)
        self.assertTrue(self.generator.session_key.startswith("🌐"))
        
        # Test NEWWORLDODOR context
        self.assertEqual(self.generator.newworldodor_context['system_id'], 'ACTNEWWORLDODOR')
        self.assertEqual(self.generator.newworldodor_context['security_level'], 'HIGH_PRIORITY')
        self.assertTrue(self.generator.newworldodor_context['allocator_access'])
    
    def test_allocator_access_setup(self):
        """Test allocator access configuration"""
        allocators = self.generator.allocator_configs
        
        self.assertIsInstance(allocators, dict)
        self.assertGreater(len(allocators), 0)
        
        # Test primary allocator (Calvin Thomas)
        self.assertIn('primary_allocator', allocators)
        primary = allocators['primary_allocator']
        self.assertEqual(primary['name'], 'Calvin Thomas')
        self.assertEqual(primary['role'], 'System Architect')
        self.assertTrue(primary['combsec_verified'])
        self.assertIn('admin', primary['permissions'])
        
        # Test other allocators have limited permissions
        for allocator_id, config in allocators.items():
            if allocator_id != 'primary_allocator':
                self.assertNotIn('admin', config['permissions'])
                self.assertFalse(config['combsec_verified'])
    
    def test_backtest_results_creation(self):
        """Test creation of backtest results from research data"""
        backtest_results = self.generator._create_backtest_results(self.sample_research_data)
        
        self.assertIsInstance(backtest_results, BacktestResult)
        self.assertEqual(backtest_results.strategy_name, "ETH Statistical Arbitrage")
        
        # Test performance metrics are within reasonable ranges
        self.assertGreaterEqual(backtest_results.total_return, 5.0)
        self.assertLessEqual(backtest_results.total_return, 10.0)  # Journal of Financial Economics range
        self.assertGreater(backtest_results.sharpe_ratio, 0)
        self.assertGreater(backtest_results.win_rate, 0)
        self.assertLess(backtest_results.win_rate, 1)
        self.assertTrue(backtest_results.peer_review_validation)
    
    def test_landing_page_generation(self):
        """Test comprehensive landing page generation"""
        page_data = self.generator.generate_backtest_sim_landing_page(self.sample_research_data)
        
        self.assertIsInstance(page_data, dict)
        self.assertIn('page_template', page_data)
        self.assertIn('backtest_results', page_data)
        self.assertIn('combsec_key', page_data)
        self.assertIn('allocator_access', page_data)
        self.assertIn('generation_timestamp', page_data)
        
        # Test page template properties
        template = page_data['page_template']
        self.assertEqual(template.title, 'QXR Backtest Sim Main Landing Page')
        self.assertEqual(template.page_type, 'comprehensive_trading_system')
        self.assertIn('VERY_IMPORTANT', template.tags)
        self.assertIn('NEWWORLDODOR', template.tags)
        self.assertIn('StatArb', template.tags)
        
        # Test content blocks
        self.assertGreater(len(template.content_blocks), 5)
        
        # Find and test key blocks
        has_performance_table = any(block.get('type') == 'table' for block in template.content_blocks)
        has_ai_workflow = any('AI WORKFLOW ACTIVE' in str(block.get('content', '')) for block in template.content_blocks)
        has_security_context = any('NEWWORLDODOR' in str(block.get('content', '')) for block in template.content_blocks)
        
        self.assertTrue(has_performance_table)
        self.assertTrue(has_ai_workflow)
        self.assertTrue(has_security_context)
    
    def test_performance_table_generation(self):
        """Test performance metrics table generation"""
        backtest_results = self.generator._create_backtest_results(self.sample_research_data)
        table_data = self.generator._generate_performance_table(backtest_results)
        
        self.assertIsInstance(table_data, list)
        self.assertGreater(len(table_data), 1)  # Header + data rows
        
        # Test header row
        self.assertEqual(table_data[0], ['Metric', 'Value', 'Peer Review Benchmark'])
        
        # Test data contains key metrics
        table_str = str(table_data)
        self.assertIn('Total Return', table_str)
        self.assertIn('Sharpe Ratio', table_str)
        self.assertIn('Max Drawdown', table_str)
        self.assertIn('JFE Studies', table_str)  # Journal of Financial Economics reference
    
    def test_allocator_table_generation(self):
        """Test allocator access table generation"""
        table_data = self.generator._generate_allocator_table()
        
        self.assertIsInstance(table_data, list)
        self.assertGreater(len(table_data), 1)  # Header + allocator rows
        
        # Test header row
        self.assertEqual(table_data[0], ['Allocator', 'Role', 'Permissions', 'COMBSEC Verified'])
        
        # Test Calvin Thomas appears as verified
        table_str = str(table_data)
        self.assertIn('Calvin Thomas', table_str)
        self.assertIn('System Architect', table_str)
        self.assertIn('✅', table_str)  # Verified marker
        
        # Test other allocators appear as pending
        self.assertIn('⚠️ Pending', table_str)
    
    def test_security_context_integration(self):
        """Test NEWWORLDODOR security context integration"""
        template = self.generator._create_landing_page_template(
            self.generator._create_backtest_results(self.sample_research_data),
            self.sample_research_data
        )
        
        template_with_security = self.generator._add_security_context(template)
        
        self.assertEqual(template_with_security.properties['newworldodor_system'], 'ACTNEWWORLDODOR')
        self.assertEqual(template_with_security.properties['security_protocol'], 'COMBSEC_U1F310')
        self.assertEqual(template_with_security.properties['priority_level'], 'HIGH_PRIORITY')
    
    def test_ai_workflow_indicators(self):
        """Test AI-driven workflow automation indicators"""
        template = self.generator._create_landing_page_template(
            self.generator._create_backtest_results(self.sample_research_data),
            self.sample_research_data
        )
        
        template_with_ai = self.generator._add_ai_workflow_indicators(template)
        
        self.assertIn('AI_AUTOMATED', template_with_ai.tags)
        self.assertTrue(template_with_ai.properties['ai_workflow_enabled'])
        
        # Test AI workflow callout is added
        ai_blocks = [block for block in template_with_ai.content_blocks 
                    if 'AI WORKFLOW ACTIVE' in str(block.get('content', ''))]
        self.assertGreater(len(ai_blocks), 0)
        
        # Test McKinsey study reference
        ai_content = str(template_with_ai.content_blocks)
        self.assertIn('McKinsey 2025', ai_content)
        self.assertIn('30% productivity', ai_content)
    
    def test_notion_markdown_generation(self):
        """Test Notion-compatible markdown generation"""
        page_data = self.generator.generate_backtest_sim_landing_page(self.sample_research_data)
        markdown_content = self.generator.generate_notion_markdown(page_data)
        
        self.assertIsInstance(markdown_content, str)
        self.assertGreater(len(markdown_content), 1000)  # Should be comprehensive
        
        # Test key sections are present
        self.assertIn('# QXR Backtest Sim Main Landing Page', markdown_content)
        self.assertIn('🚨 **VERY IMPORTANT**', markdown_content)
        self.assertIn('## 📊 Statistical Arbitrage Performance Summary', markdown_content)
        self.assertIn('## 🔬 Peer-Reviewed Validation', markdown_content)
        self.assertIn('## 🔐 NEWWORLDODOR Security Context', markdown_content)
        self.assertIn('## 🤖 AI-Driven Workflow Automation', markdown_content)
        self.assertIn('## 👥 Multi-Allocator Shared Access', markdown_content)
        
        # Test COMBSEC key inclusion
        self.assertIn('COMBSEC Key:', markdown_content)
        self.assertIn('🌐-', markdown_content)
        
        # Test allocator table
        self.assertIn('Calvin Thomas', markdown_content)
        self.assertIn('System Architect', markdown_content)
        
        # Test peer review references
        self.assertIn('Journal of Financial Economics', markdown_content)
        self.assertIn('5-10%', markdown_content)
    
    def test_page_spec_saving(self):
        """Test saving page specification to file"""
        with tempfile.TemporaryDirectory() as temp_dir:
            page_data = self.generator.generate_backtest_sim_landing_page(self.sample_research_data)
            spec_file = self.generator.save_notion_page_spec(page_data, temp_dir)
            
            self.assertTrue(os.path.exists(spec_file))
            self.assertTrue(spec_file.endswith('.json'))
            
            # Test file content
            with open(spec_file, 'r') as f:
                spec_data = json.load(f)
            
            self.assertIn('metadata', spec_data)
            self.assertIn('page_template', spec_data)
            self.assertIn('backtest_results', spec_data)
            self.assertIn('allocator_access', spec_data)
            self.assertIn('implementation_notes', spec_data)
            
            # Test metadata
            self.assertEqual(spec_data['metadata']['priority'], 'VERY_IMPORTANT')
            self.assertEqual(spec_data['metadata']['context'], 'NEWWORLDODOR')
            
            # Test implementation notes
            self.assertIn('notion_api_version', spec_data['implementation_notes'])
            self.assertIn('required_permissions', spec_data['implementation_notes'])
            self.assertIn('security_notes', spec_data['implementation_notes'])


class TestEnhancedSocialMediaEngine(unittest.TestCase):
    """Test the enhanced social media engine with Notion page generation"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.engine = SocialMediaEngine("TESTENHANCED")
        self.sample_research_data = {
            'signals': 45,
            'opportunities': 8,
            'signal_strength': 1.247,
            'price_range': [3420, 3580],
            'max_liquidity': 12500000,
            'strategy': 'ETH Statistical Arbitrage',
            'timeframe': '24h'
        }
    
    def test_enhanced_engine_initialization(self):
        """Test enhanced engine initialization with Notion generator"""
        self.assertIsNotNone(self.engine.notion_generator)
        self.assertIsInstance(self.engine.notion_generator, NotionPageGenerator)
        self.assertEqual(self.engine.notion_generator.firm_id, "TESTENHANCED")
    
    def test_notion_landing_page_integration(self):
        """Test Notion landing page integration in one-push workflow"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Override save method to use temp directory
            original_save = self.engine.save_posts_for_manual_publishing
            
            def mock_save(posts):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                master_file = os.path.join(temp_dir, f"test_posts_{timestamp}.md")
                return master_file
            
            self.engine.save_posts_for_manual_publishing = mock_save
            
            # Test with Notion in target platforms
            master_file, posts = self.engine.one_push_manual_prepare(
                self.sample_research_data,
                target_platforms=['linkedin', 'notion']
            )
            
            self.assertIn('notion', posts)
            self.assertIn('linkedin', posts)
            
            # Test Notion content is comprehensive (landing page, not simple post)
            notion_content = posts['notion']
            self.assertIn('# QXR Backtest Sim Main Landing Page', notion_content)
            self.assertIn('🚨 **VERY IMPORTANT**', notion_content)
            self.assertIn('Statistical Arbitrage Performance Summary', notion_content)
            self.assertIn('NEWWORLDODOR Security Context', notion_content)
            self.assertIn('Multi-Allocator Shared Access', notion_content)
            self.assertIn('Calvin Thomas', notion_content)
            
            # Test history includes landing page information
            self.assertGreater(len(self.engine.post_history), 0)
            last_entry = self.engine.post_history[-1]
            if 'notion_landing_page' in last_entry:
                self.assertTrue(last_entry['notion_landing_page']['has_backtest_sim'])
                self.assertGreater(last_entry['notion_landing_page']['allocator_count'], 0)
    
    def test_enhanced_posting_instructions(self):
        """Test enhanced posting instructions include Notion landing page info"""
        instructions = self.engine.get_posting_instructions()
        
        self.assertIn('BACKTEST SIM LANDING PAGE', instructions)
        self.assertIn('VERY IMPORTANT', instructions)
        self.assertIn('Journal of Financial Economics', instructions)
        self.assertIn('NEWWORLDODOR', instructions)
        self.assertIn('allocator permissions', instructions)
        self.assertIn('AI-driven workflow', instructions)


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
    suite.addTest(unittest.makeSuite(TestNotionPageGenerator))
    suite.addTest(unittest.makeSuite(TestEnhancedSocialMediaEngine))
    
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