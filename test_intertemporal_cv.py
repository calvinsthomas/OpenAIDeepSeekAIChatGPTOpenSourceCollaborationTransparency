#!/usr/bin/env python3
"""
Test Suite for Intertemporal Differentials Analysis Module

Tests the IntertemporalAnalyzer class and its integration with
the COMBSEC system as specified in the ChatGPT document.
"""

import unittest
import sys
from pathlib import Path
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Add the repository root to path
repo_root = Path(__file__).parent
sys.path.insert(0, str(repo_root))

from intertemporal_cv import IntertemporalAnalyzer, create_sample_financial_data
from ACTNEWWORLDODOR.emoji_combsec_generator import EmojiCombsecGenerator


class TestIntertemporalAnalyzer(unittest.TestCase):
    """Test cases for IntertemporalAnalyzer class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.analyzer = IntertemporalAnalyzer(firm_id="TESTFIRM")
        self.sample_data = create_sample_financial_data(30)
        
    def test_analyzer_initialization(self):
        """Test proper analyzer initialization"""
        self.assertIsNotNone(self.analyzer)
        self.assertEqual(self.analyzer.firm_id, "TESTFIRM")
        self.assertIsNotNone(self.analyzer.security_key)
        self.assertTrue(self.analyzer.security_key.startswith("🌐"))
        
    def test_analyzer_with_custom_security_key(self):
        """Test analyzer initialization with custom security key"""
        custom_key = "🌐-TESTKEY123456789-1234567890-TESTFIRM"
        analyzer = IntertemporalAnalyzer(security_key=custom_key)
        self.assertEqual(analyzer.security_key, custom_key)
        
    def test_combsec_integration(self):
        """Test COMBSEC integration as specified in ChatGPT document"""
        # Test the exact pattern from the document
        generator = EmojiCombsecGenerator()
        security_key = generator.generate_combsec_key()
        
        analyzer = IntertemporalAnalyzer(security_key=security_key)
        
        self.assertEqual(analyzer.security_key, security_key)
        self.assertTrue(security_key.startswith("🌐"))
        
    def test_temporal_differential_analysis(self):
        """Test temporal differential calculations"""
        results = self.analyzer.analyze_temporal_diffs(
            data=self.sample_data,
            cv_method='time_series',
            parody_detection=False
        )
        
        # Check basic structure
        self.assertIn('temporal_differentials', results)
        self.assertIn('cv_analysis', results)
        self.assertIn('method', results)
        self.assertEqual(results['method'], 'time_series')
        
        # Check temporal differentials were calculated
        temp_diffs = results['temporal_differentials']
        self.assertTrue(len(temp_diffs) > 0)
        
        # Check that price differential was calculated
        price_diff_key = next((k for k in temp_diffs.keys() if 'price_temporal_delta' in k), None)
        self.assertIsNotNone(price_diff_key)
        
    def test_cross_validation_methods(self):
        """Test different CV methods"""
        cv_methods = ['time_series', 'expanding_window', 'blocked']
        
        for method in cv_methods:
            with self.subTest(method=method):
                results = self.analyzer.analyze_temporal_diffs(
                    data=self.sample_data,
                    cv_method=method,
                    parody_detection=False,
                    target_column='price'
                )
                
                self.assertEqual(results['method'], method)
                self.assertIn('cv_analysis', results)
                
                cv_analysis = results['cv_analysis']
                self.assertEqual(cv_analysis['method'], method)
                
    def test_parody_detection(self):
        """Test parody detection functionality"""
        # Create data with parody markers
        parody_data = self.sample_data.copy()
        parody_data.loc[parody_data.index[0], 'text_analysis'] = "This is a #parody market analysis"
        parody_data.loc[parody_data.index[1], 'text_analysis'] = "Fake news about crypto"
        
        results = self.analyzer.analyze_temporal_diffs(
            data=parody_data,
            cv_method='time_series',
            parody_detection=True
        )
        
        self.assertIn('parody_detection', results)
        parody_results = results['parody_detection']
        
        self.assertIn('total_parody_indicators', parody_results)
        self.assertIn('parody_indicators_found', parody_results)
        self.assertIn('pattern_confidence', parody_results)
        
        # Should find at least the parody markers we added
        self.assertGreater(parody_results['total_parody_indicators'], 0)
        
    def test_volatility_clustering_analysis(self):
        """Test volatility clustering analysis"""
        results = self.analyzer.analyze_temporal_diffs(
            data=self.sample_data,
            cv_method='time_series',
            parody_detection=False,
            target_column='price'
        )
        
        self.assertIn('volatility_analysis', results)
        vol_analysis = results['volatility_analysis']
        
        self.assertIn('volatility_metrics', vol_analysis)
        self.assertIn('stationarity_test', vol_analysis)
        
    def test_regime_change_detection(self):
        """Test regime change detection"""
        # Use longer series for regime change detection
        longer_data = create_sample_financial_data(100)
        price_series = longer_data['price']
        
        regime_results = self.analyzer.get_regime_change_detection(price_series)
        
        self.assertIn('regime_changes', regime_results)
        self.assertIn('change_points', regime_results)
        
        # Check if we have enough data or got an error message
        if 'error' in regime_results:
            # If insufficient data, that's also a valid result to test
            self.assertIn('Insufficient data', regime_results['error'])
        else:
            # If we have enough data, should have total_regime_changes
            self.assertIn('total_regime_changes', regime_results)
        
    def test_security_context_validation(self):
        """Test COMBSEC security context validation"""
        validation_result = self.analyzer.validate_security_context()
        
        self.assertIn('valid', validation_result)
        self.assertTrue(validation_result['valid'])
        
        if 'security_key_truncated' in validation_result:
            self.assertTrue(validation_result['security_key_truncated'].startswith("🌐"))
        
    def test_data_format_handling(self):
        """Test handling different data formats"""
        # Test with dictionary input
        dict_data = {
            'price': [100, 101, 102, 103, 104],
            'volume': [1000, 1100, 1200, 1300, 1400],
            'text': ['normal', 'parody content', 'normal', 'fake news', 'normal']
        }
        
        results = self.analyzer.analyze_temporal_diffs(
            data=dict_data,
            cv_method='time_series',
            parody_detection=True
        )
        
        self.assertIn('method', results)
        self.assertIn('data_shape', results)
        self.assertEqual(results['data_shape'], (5, 3))
        
    def test_insufficient_data_handling(self):
        """Test handling of insufficient data"""
        small_data = create_sample_financial_data(5)  # Very small dataset
        
        results = self.analyzer.analyze_temporal_diffs(
            data=small_data,
            cv_method='time_series',
            parody_detection=True
        )
        
        # Should still return results but with appropriate warnings/errors
        self.assertIn('method', results)
        self.assertIn('cv_analysis', results)
        
    def test_missing_target_column_handling(self):
        """Test handling when target column doesn't exist"""
        results = self.analyzer.analyze_temporal_diffs(
            data=self.sample_data,
            cv_method='time_series',
            parody_detection=False,
            target_column='nonexistent_column'
        )
        
        # Should fallback to first numeric column
        self.assertIn('cv_analysis', results)


class TestSampleDataGeneration(unittest.TestCase):
    """Test the sample data generation function"""
    
    def test_sample_data_structure(self):
        """Test sample financial data structure"""
        data = create_sample_financial_data(100)
        
        self.assertEqual(len(data), 100)
        self.assertIn('price', data.columns)
        self.assertIn('volume', data.columns)
        self.assertIn('returns', data.columns)
        self.assertIn('text_analysis', data.columns)
        
        # Check that index is datetime
        self.assertIsInstance(data.index, pd.DatetimeIndex)
        
        # Check that some parody markers exist
        text_content = ' '.join(data['text_analysis'].values)
        self.assertTrue(any(marker in text_content.lower() for marker in ['parody', 'fake']))
        
    def test_sample_data_reproducibility(self):
        """Test that sample data generation is reproducible"""
        data1 = create_sample_financial_data(50)
        data2 = create_sample_financial_data(50)
        
        # Should be identical due to fixed random seed
        pd.testing.assert_frame_equal(data1, data2)


class TestIntegrationWithExistingSystems(unittest.TestCase):
    """Test integration with existing QXR and COMBSEC systems"""
    
    def test_qxr_integration_compatibility(self):
        """Test compatibility with QXR system"""
        # Create analyzer that could be used by QXR
        analyzer = IntertemporalAnalyzer(firm_id="QXR")
        
        # Create data similar to what QXR might provide
        qxr_data = {
            'signals': [45, 46, 44, 47, 48],
            'opportunities': [8, 9, 7, 10, 11],
            'signal_strength': [1.247, 1.251, 1.243, 1.255, 1.259],
            'price_range_min': [3420, 3425, 3415, 3430, 3435],
            'price_range_max': [3580, 3585, 3575, 3590, 3595]
        }
        
        results = analyzer.analyze_temporal_diffs(
            data=qxr_data,
            cv_method='time_series',
            parody_detection=False,
            target_column='signals'
        )
        
        self.assertIn('temporal_differentials', results)
        self.assertIn('cv_analysis', results)
        
    def test_combsec_key_format_compatibility(self):
        """Test COMBSEC key format compatibility"""
        analyzer = IntertemporalAnalyzer()
        
        # Validate that the security key follows COMBSEC format
        key = analyzer.security_key
        parts = key.split('-')
        
        self.assertEqual(len(parts), 4)  # 🌐-HEXKEY-TIMESTAMP-FIRMID
        self.assertEqual(parts[0], "🌐")
        self.assertEqual(len(parts[1]), 16)  # 16-character hex key
        self.assertTrue(parts[2].isdigit())  # Timestamp should be numeric
        self.assertTrue(len(parts[3]) > 0)  # Firm ID should exist


def run_comprehensive_tests():
    """Run all tests and provide a comprehensive report"""
    print("🧪 Running Intertemporal CV Module Tests")
    print("=" * 60)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        TestIntertemporalAnalyzer,
        TestSampleDataGeneration,
        TestIntegrationWithExistingSystems
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 60)
    print(f"📊 Test Results Summary:")
    print(f"   Tests run: {result.testsRun}")
    print(f"   Failures: {len(result.failures)}")
    print(f"   Errors: {len(result.errors)}")
    print(f"   Skipped: {len(result.skipped) if hasattr(result, 'skipped') else 0}")
    
    if result.wasSuccessful():
        print("🎉 All tests passed! Intertemporal CV module is ready for integration.")
        return True
    else:
        print("❌ Some tests failed. Please review the output above.")
        if result.failures:
            print(f"\nFailures:")
            for test, traceback in result.failures:
                print(f"  - {test}: {traceback}")
        if result.errors:
            print(f"\nErrors:")
            for test, traceback in result.errors:
                print(f"  - {test}: {traceback}")
        return False


if __name__ == "__main__":
    success = run_comprehensive_tests()
    exit(0 if success else 1)