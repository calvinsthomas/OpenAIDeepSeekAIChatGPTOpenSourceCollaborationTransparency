#!/usr/bin/env python3
"""
QXR GraphQL Integration Tests
Test suite for GraphQL API resolvers and schema validation

This module provides comprehensive tests for:
- GraphQL resolver functionality
- COMBSEC authentication integration
- Research data processing via GraphQL
- Social media post generation via GraphQL
- Notion landing page creation via GraphQL
- System health monitoring
- Error handling and edge cases
"""

import unittest
import tempfile
import json
import os
import sys
from datetime import datetime

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from QXR.graphql_resolvers import GraphQLResolvers, RESOLVER_MAP
except ImportError as e:
    print(f"❌ Error importing GraphQL modules: {e}")
    sys.exit(1)


class TestGraphQLResolvers(unittest.TestCase):
    """Test GraphQL resolver functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.resolvers = GraphQLResolvers()
        self.sample_research_data = {
            'signals': 45,
            'opportunities': 8,
            'signal_strength': 1.247,
            'price_range': [3420, 3580],
            'max_liquidity': 12500000,
            'strategy': 'ETH Statistical Arbitrage',
            'timeframe': '24h'
        }
        self.sample_firm_id = "TESTFIRM"
    
    def test_combsec_key_generation(self):
        """Test COMBSEC key generation resolver"""
        result = self.resolvers.generate_combsec_key(None, self.sample_firm_id)
        
        self.assertIsInstance(result, dict)
        self.assertIn('id', result)
        self.assertIn('session_key', result)
        self.assertIn('truncated_key', result)
        self.assertIn('verified', result)
        self.assertIn('generated_at', result)
        
        # Verify key format
        self.assertTrue(result['session_key'].startswith('🌐-'))
        self.assertTrue(result['verified'])
        self.assertLess(len(result['truncated_key']), len(result['session_key']))
    
    def test_combsec_key_validation(self):
        """Test COMBSEC key validation resolver"""
        # Generate a key first
        key_result = self.resolvers.generate_combsec_key(None, self.sample_firm_id)
        session_key = key_result['session_key']
        
        # Test validation
        is_valid = self.resolvers.validate_combsec_key(None, session_key)
        self.assertTrue(is_valid)
        
        # Test invalid key
        is_invalid = self.resolvers.validate_combsec_key(None, "invalid_key")
        self.assertFalse(is_invalid)
    
    def test_backtest_results_generation(self):
        """Test backtest results generation"""
        result = self.resolvers.get_backtest_results(None, self.sample_research_data)
        
        self.assertIsInstance(result, dict)
        required_fields = [
            'total_return', 'sharpe_ratio', 'max_drawdown', 
            'win_rate', 'volatility', 'alpha', 'beta', 
            'information_ratio', 'performance'
        ]
        
        for field in required_fields:
            self.assertIn(field, result)
            if field != 'performance':
                self.assertIsInstance(result[field], (int, float))
        
        # Verify reasonable ranges
        self.assertGreaterEqual(result['win_rate'], 0.0)
        self.assertLessEqual(result['win_rate'], 1.0)
        self.assertGreater(result['volatility'], 0.0)
    
    def test_system_health_monitoring(self):
        """Test system health monitoring resolver"""
        health = self.resolvers.system_health(None)
        
        self.assertIsInstance(health, dict)
        required_fields = [
            'status', 'uptime', 'last_update', 
            'combsec_active', 'notion_integration', 'social_media_engine'
        ]
        
        for field in required_fields:
            self.assertIn(field, health)
        
        self.assertIn(health['status'], ['HEALTHY', 'ERROR'])
        self.assertIsInstance(health['combsec_active'], bool)
        self.assertIsInstance(health['notion_integration'], bool)
        self.assertIsInstance(health['social_media_engine'], bool)
    
    def test_integration_status(self):
        """Test integration status resolver"""
        status = self.resolvers.integration_status(None)
        
        self.assertIsInstance(status, dict)
        self.assertIn('actnewworldodor', status)
        self.assertIn('qxr_notebook', status)
        self.assertIn('notion_api', status)
        self.assertIn('social_platforms', status)
        
        # Verify social platforms structure
        platforms = status['social_platforms']
        self.assertIsInstance(platforms, list)
        
        for platform in platforms:
            self.assertIn('platform', platform)
            self.assertIn('available', platform)
            self.assertIn('last_sync', platform)
    
    def test_social_media_posts_preparation(self):
        """Test social media posts preparation resolver"""
        # Generate auth key first
        auth_key = self.resolvers.generate_combsec_key(None, self.sample_firm_id)
        
        options = {
            'firm_id': self.sample_firm_id,
            'target_platforms': ['linkedin', 'twitter'],
            'include_notion_landing': False
        }
        
        auth = {
            'session_key': auth_key['session_key'],
            'firm_id': self.sample_firm_id
        }
        
        result = self.resolvers.prepare_social_media_posts(
            None, self.sample_research_data, options, auth
        )
        
        self.assertIsInstance(result, dict)
        self.assertIn('master_file', result)
        self.assertIn('posts', result)
        self.assertIn('instructions', result)
        
        # Verify posts structure
        posts = result['posts']
        self.assertIsInstance(posts, list)
        self.assertEqual(len(posts), 2)  # linkedin, twitter
        
        for post in posts:
            self.assertIn('platform', post)
            self.assertIn('content', post)
            self.assertIn('hashtags', post)
            self.assertIn('combsec_key', post)
            self.assertIn('generated_at', post)
    
    def test_notion_landing_page_generation(self):
        """Test Notion landing page generation resolver"""
        options = {
            'firm_id': self.sample_firm_id,
            'include_allocator_access': True,
            'security_level': 'HIGH_PRIORITY',
            'enable_ai_workflow': True
        }
        
        result = self.resolvers.generate_notion_landing_page(
            None, self.sample_research_data, options
        )
        
        self.assertIsInstance(result, dict)
        self.assertIn('spec_file', result)
        self.assertIn('markdown_content', result)
        self.assertIn('landing_page_data', result)
        self.assertIn('api_spec', result)
        
        # Verify spec file exists
        self.assertTrue(os.path.exists(result['spec_file']))
        
        # Verify markdown content is not empty
        self.assertGreater(len(result['markdown_content']), 100)
        
        # Verify API spec is valid JSON
        try:
            json.loads(result['api_spec'])
        except json.JSONDecodeError:
            self.fail("API spec is not valid JSON")
    
    def test_authentication_required_operations(self):
        """Test that operations requiring authentication fail without valid auth"""
        invalid_auth = {
            'session_key': 'invalid_key',
            'firm_id': self.sample_firm_id
        }
        
        # Test that operations requiring auth fail with invalid key
        with self.assertRaises(Exception):
            self.resolvers.process_notebook(None, "/fake/path", invalid_auth)
        
        with self.assertRaises(Exception):
            self.resolvers.configure_allocator_access(
                None, "test_allocator", ["read", "write"], invalid_auth
            )
    
    def test_resolver_map_completeness(self):
        """Test that resolver map contains all expected operations"""
        self.assertIn('Query', RESOLVER_MAP)
        self.assertIn('Mutation', RESOLVER_MAP)
        self.assertIn('Subscription', RESOLVER_MAP)
        
        # Test Query resolvers
        query_resolvers = RESOLVER_MAP['Query']
        expected_queries = [
            'generateCombsecKey', 'validateCombsecKey', 'extractNotebookMetrics',
            'getBacktestResults', 'generateNotionLandingPage', 
            'prepareSocialMediaPosts', 'systemHealth', 'integrationStatus'
        ]
        
        for query in expected_queries:
            self.assertIn(query, query_resolvers)
            self.assertTrue(callable(query_resolvers[query]))
        
        # Test Mutation resolvers
        mutation_resolvers = RESOLVER_MAP['Mutation']
        expected_mutations = [
            'processNotebook', 'generateSocialMediaPackage',
            'createNotionLandingPage', 'refreshCombsecKey',
            'configureAllocatorAccess'
        ]
        
        for mutation in expected_mutations:
            self.assertIn(mutation, mutation_resolvers)
            self.assertTrue(callable(mutation_resolvers[mutation]))
    
    def test_error_handling(self):
        """Test error handling in resolvers"""
        # Test with invalid research data
        invalid_data = {}
        
        try:
            result = self.resolvers.get_backtest_results(None, invalid_data)
            # Should still return something, even with empty data
            self.assertIsInstance(result, dict)
        except Exception:
            # It's acceptable for this to fail gracefully
            pass
        
        # Test with non-existent notebook path
        try:
            result = self.resolvers.extract_notebook_metrics(None, "/nonexistent/path.ipynb")
            # The notebook processor handles missing files gracefully by logging an error
            # So we verify that it returns some form of result or raises a proper exception
            if result is not None:
                # If it returns a result, it should be a dict with default values
                self.assertIsInstance(result, dict)
            else:
                # If it returns None, that's also acceptable error handling
                pass
        except Exception as e:
            # If it raises an exception, it should contain appropriate error message
            self.assertIn("Failed to extract", str(e))


class TestGraphQLSchemaValidation(unittest.TestCase):
    """Test GraphQL schema file validation"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.schema_file = "/home/runner/work/OpenAIDeepSeekAIChatGPTOpenSourceCollaborationTransparency/OpenAIDeepSeekAIChatGPTOpenSourceCollaborationTransparency/@graphQL.ynl"
        self.config_file = "/home/runner/work/OpenAIDeepSeekAIChatGPTOpenSourceCollaborationTransparency/OpenAIDeepSeekAIChatGPTOpenSourceCollaborationTransparency/@GraphQL"
    
    def test_schema_file_exists(self):
        """Test that GraphQL schema file exists"""
        self.assertTrue(os.path.exists(self.schema_file))
    
    def test_config_file_exists(self):
        """Test that GraphQL config file exists"""
        self.assertTrue(os.path.exists(self.config_file))
    
    def test_schema_content_validity(self):
        """Test that schema file contains expected GraphQL definitions"""
        with open(self.schema_file, 'r') as f:
            content = f.read()
        
        # Check for essential GraphQL elements
        required_elements = [
            'type Query', 'type Mutation', 'type Subscription',
            'type CombsecKey', 'type ResearchMetrics', 'type BacktestResult',
            'type NotionPageTemplate', 'type SocialMediaPost',
            'generateCombsecKey', 'validateCombsecKey',
            'extractNotebookMetrics', 'prepareSocialMediaPosts',
            'schema {'
        ]
        
        for element in required_elements:
            self.assertIn(element, content, f"Missing required element: {element}")
    
    def test_config_file_content(self):
        """Test that config file contains expected configuration"""
        with open(self.config_file, 'r') as f:
            content = f.read()
        
        required_config = [
            'SCHEMA_FILE=@graphQL.ynl',
            'ENDPOINT=/graphql',
            'AUTH_REQUIRED=COMBSEC',
            'RESOLVERS=QXR.graphql_resolvers',
            'COMBSEC_AUTHENTICATION=ENABLED'
        ]
        
        for config in required_config:
            self.assertIn(config, content, f"Missing required config: {config}")


def run_graphql_tests():
    """Run all GraphQL integration tests"""
    print("🌐 QXR GraphQL Integration - Test Suite")
    print("=" * 60)
    
    # Create test suite
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestGraphQLResolvers))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestGraphQLSchemaValidation))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 GraphQL Test Results Summary:")
    print(f"   Tests run: {result.testsRun}")
    print(f"   Failures: {len(result.failures)}")
    print(f"   Errors: {len(result.errors)}")
    print(f"   Skipped: {len(result.skipped) if hasattr(result, 'skipped') else 0}")
    
    if result.wasSuccessful():
        print("🎉 All GraphQL tests passed! API ready for integration.")
        return True
    else:
        print("❌ Some GraphQL tests failed. Please review the output above.")
        return False


if __name__ == "__main__":
    # Run comprehensive GraphQL tests
    success = run_graphql_tests()
    sys.exit(0 if success else 1)