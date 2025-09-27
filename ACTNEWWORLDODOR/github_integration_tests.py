#!/usr/bin/env python3
"""
GitHub Integration Tests for COMBSEC System
Tests the "ALL MONEY IN! TIMESTAMP ME GH!" functionality
"""

import sys
import os
import json
import time
from datetime import datetime

# Add the ACTNEWWORLDODOR directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from github_timestamp_integration import (
    GitHubTimestampIntegrator, 
    generate_github_combsec_key_u1f310
)
from emoji_combsec_generator import EmojiCombsecGenerator

def test_github_integrator_initialization():
    """Test GitHub integrator initialization"""
    print("🔧 Testing GitHub integrator initialization...")
    
    integrator = GitHubTimestampIntegrator("TEST_FIRM")
    
    assert integrator.firm_id == "TEST_FIRM", "Firm ID not set correctly"
    assert integrator.combsec_generator is not None, "COMBSEC generator not initialized"
    assert integrator.combsec_generator.firm_id == "TEST_FIRM", "Generator firm ID mismatch"
    
    print("✅ GitHub integrator initialization test passed")
    return True

def test_git_commit_info_extraction():
    """Test Git commit information extraction"""
    print("📝 Testing Git commit info extraction...")
    
    integrator = GitHubTimestampIntegrator("TEST_FIRM")
    git_info = integrator.get_git_commit_info()
    
    # Check required fields exist
    required_fields = ["commit_hash", "commit_timestamp", "commit_author", 
                      "commit_message", "commit_datetime"]
    
    for field in required_fields:
        assert field in git_info, f"Missing field: {field}"
    
    # Validate timestamp is reasonable
    assert isinstance(git_info["commit_timestamp"], int), "Timestamp should be integer"
    assert git_info["commit_timestamp"] > 0, "Timestamp should be positive"
    
    print(f"✅ Git info extracted: {git_info['commit_hash'][:8]}...")
    return True

def test_github_environment_info():
    """Test GitHub environment information extraction"""
    print("🌐 Testing GitHub environment info extraction...")
    
    integrator = GitHubTimestampIntegrator("TEST_FIRM")
    github_env = integrator.get_github_environment_info()
    
    # Check that function returns expected structure
    assert isinstance(github_env, dict), "GitHub env should be a dictionary"
    
    expected_keys = ['github_actor', 'github_repository', 'github_ref', 
                    'github_sha', 'github_workflow', 'github_run_id']
    
    for key in expected_keys:
        assert key in github_env, f"Missing GitHub env key: {key}"
    
    print("✅ GitHub environment info extraction test passed")
    return True

def test_github_timestamped_key_generation():
    """Test GitHub-enhanced COMBSEC key generation"""
    print("🔑 Testing GitHub-timestamped key generation...")
    
    integrator = GitHubTimestampIntegrator("GITHUB_TEST_FIRM")
    key_data = integrator.generate_github_timestamped_key()
    
    # Validate key data structure
    required_keys = ["combsec_key", "github_metadata", "entropy_source", "firm_id"]
    for key in required_keys:
        assert key in key_data, f"Missing key data field: {key}"
    
    # Validate the COMBSEC key format
    combsec_key = key_data["combsec_key"]
    assert combsec_key.startswith("🌐-"), "Key should start with globe emoji"
    
    parts = combsec_key.split('-')
    assert len(parts) == 4, "Key should have 4 parts"
    assert parts[3] == "GITHUB_TEST_FIRM", "Firm ID should match"
    
    # Validate metadata
    metadata = key_data["github_metadata"]
    assert "generation_timestamp" in metadata, "Missing generation timestamp"
    assert "generation_datetime" in metadata, "Missing generation datetime"
    
    print(f"✅ Generated GitHub key: {combsec_key}")
    return True

def test_github_key_validation():
    """Test GitHub-enhanced key validation"""
    print("🔍 Testing GitHub key validation...")
    
    integrator = GitHubTimestampIntegrator("VALIDATION_TEST_FIRM")
    key_data = integrator.generate_github_timestamped_key()
    
    validation = integrator.validate_github_timestamped_key(key_data)
    
    # Check validation results
    assert validation["valid"] == True, "Key validation should pass"
    assert validation.get("github_enhanced", False) == True, "Should be GitHub enhanced"
    assert "entropy_source" in validation, "Should include entropy source"
    
    print("✅ GitHub key validation test passed")
    return True

def test_invalid_github_key_handling():
    """Test handling of invalid GitHub key data"""
    print("⚠️ Testing invalid GitHub key handling...")
    
    integrator = GitHubTimestampIntegrator("TEST_FIRM")
    
    # Test various invalid inputs
    invalid_inputs = [
        {},  # Empty dict
        {"invalid": "data"},  # Missing combsec_key
        {"combsec_key": "invalid-key-format"},  # Invalid key format
    ]
    
    for invalid_input in invalid_inputs:
        validation = integrator.validate_github_timestamped_key(invalid_input)
        assert validation["valid"] == False, f"Should reject invalid input: {invalid_input}"
    
    print("✅ Invalid key handling test passed")
    return True

def test_github_api_function():
    """Test the standardized GitHub API function"""
    print("🚀 Testing generate_github_combsec_key_u1f310 API function...")
    
    # Test basic functionality
    key1 = generate_github_combsec_key_u1f310("API_TEST_FIRM")
    assert key1.startswith("🌐-"), "API key should start with globe emoji"
    assert key1.endswith("-API_TEST_FIRM"), "API key should end with firm ID"
    
    # Test with different parameters
    key2 = generate_github_combsec_key_u1f310("API_FIRM_2", include_commit_data=False)
    key3 = generate_github_combsec_key_u1f310("API_FIRM_3", include_github_env=False)
    
    # Keys should be different
    assert key1 != key2, "Keys should be unique"
    assert key1 != key3, "Keys should be unique"
    assert key2 != key3, "Keys should be unique"
    
    print(f"✅ API function test passed")
    print(f"   Key 1: {key1}")
    print(f"   Key 2: {key2}")
    print(f"   Key 3: {key3}")
    return True

def test_github_key_batch_export():
    """Test GitHub key batch generation and export"""
    print("📦 Testing GitHub key batch export...")
    
    integrator = GitHubTimestampIntegrator("BATCH_TEST_FIRM")
    batch_data = integrator.export_github_key_batch(3)
    
    # Validate batch structure
    assert "system" in batch_data, "Missing system field"
    assert "total_keys" in batch_data, "Missing total_keys field"
    assert "keys" in batch_data, "Missing keys field"
    assert "github_integration" in batch_data, "Missing github_integration field"
    
    # Validate keys
    assert batch_data["total_keys"] == 3, "Should have 3 keys"
    assert len(batch_data["keys"]) == 3, "Keys array should have 3 items"
    assert batch_data["github_integration"] == True, "Should be GitHub integrated"
    
    # Validate each key in the batch
    for i, key_data in enumerate(batch_data["keys"]):
        validation = integrator.validate_github_timestamped_key(key_data)
        assert validation["valid"] == True, f"Batch key {i} should be valid"
    
    print(f"✅ Generated and validated batch of {batch_data['total_keys']} keys")
    return True

def test_comprehensive_github_integration():
    """Test comprehensive GitHub integration functionality"""
    print("🌟 Testing comprehensive GitHub integration...")
    
    # Test the "ALL MONEY IN! TIMESTAMP ME GH!" functionality
    integrator = GitHubTimestampIntegrator("COMPREHENSIVE_FIRM")
    
    # Generate multiple keys with different configurations
    configurations = [
        {"include_commit_data": True, "include_github_env": True},
        {"include_commit_data": True, "include_github_env": False},
        {"include_commit_data": False, "include_github_env": True},
        {"include_commit_data": False, "include_github_env": False},
    ]
    
    keys_generated = []
    
    for i, config in enumerate(configurations):
        key_data = integrator.generate_github_timestamped_key(**config)
        keys_generated.append(key_data)
        
        # Validate each key
        validation = integrator.validate_github_timestamped_key(key_data)
        assert validation["valid"] == True, f"Config {i} key should be valid"
        
        # Check metadata based on configuration
        metadata = key_data["github_metadata"]
        
        if config["include_commit_data"]:
            assert "git_info" in metadata, f"Config {i} should include git_info"
        
        if config["include_github_env"]:
            assert "github_env" in metadata, f"Config {i} should include github_env"
    
    # Ensure all keys are unique
    combsec_keys = [kd["combsec_key"] for kd in keys_generated]
    assert len(set(combsec_keys)) == len(combsec_keys), "All keys should be unique"
    
    print(f"✅ Comprehensive integration test passed with {len(keys_generated)} configurations")
    return True

def run_github_integration_tests():
    """Run all GitHub integration tests"""
    print("🌐 COMBSEC GitHub Integration Tests")
    print("=" * 60)
    print("Testing 'ALL MONEY IN! TIMESTAMP ME GH!' functionality")
    print("=" * 60)
    
    tests = [
        test_github_integrator_initialization,
        test_git_commit_info_extraction,
        test_github_environment_info,
        test_github_timestamped_key_generation,
        test_github_key_validation,
        test_invalid_github_key_handling,
        test_github_api_function,
        test_github_key_batch_export,
        test_comprehensive_github_integration,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"❌ {test.__name__} failed: {str(e)}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"🎯 GitHub Integration Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 ALL MONEY IN! GitHub integration fully operational!")
        print("✅ TIMESTAMP ME - Enhanced timestamping active")
        print("✅ GH! - GitHub functionality complete")
        return True
    else:
        print("💥 Some GitHub integration tests failed. Please review.")
        return False


if __name__ == "__main__":
    # Run all GitHub integration tests
    success = run_github_integration_tests()
    sys.exit(0 if success else 1)