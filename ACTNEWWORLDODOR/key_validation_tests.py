#!/usr/bin/env python3
"""
ACTNEWWORLDODOR - COMBSEC Key Validation Tests
Simple test suite for the emoji-based combinatoric security key system
"""

import sys
import os

# Add the ACTNEWWORLDODOR directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from emoji_combsec_generator import EmojiCombsecGenerator, generate_combsec_key_u1f310

def test_key_generation():
    """Test basic key generation functionality"""
    print("🧪 Testing key generation...")
    
    generator = EmojiCombsecGenerator("TESTFIRM")
    key = generator.generate_combsec_key()
    
    # Basic format validation
    parts = key.split('-')
    assert len(parts) == 4, f"Expected 4 parts, got {len(parts)}"
    assert parts[0] == "🌐", f"Expected globe emoji, got {parts[0]}"
    assert len(parts[1]) == 16, f"Expected 16-char hex key, got {len(parts[1])}"
    assert parts[3] == "TESTFIRM", f"Expected TESTFIRM, got {parts[3]}"
    
    print(f"✅ Generated key: {key}")
    return True

def test_key_validation():
    """Test key validation functionality"""
    print("🔍 Testing key validation...")
    
    generator = EmojiCombsecGenerator("TESTFIRM")
    key = generator.generate_combsec_key()
    
    validation = generator.validate_combsec_key(key)
    assert validation["valid"] == True, "Key validation failed"
    assert validation["emoji"] == "🌐", "Emoji validation failed"
    assert validation["firm_id"] == "TESTFIRM", "Firm ID validation failed"
    
    print(f"✅ Key validation passed: {validation['valid']}")
    return True

def test_batch_generation():
    """Test batch key generation"""
    print("📦 Testing batch key generation...")
    
    generator = EmojiCombsecGenerator("TESTFIRM")
    batch = generator.generate_key_batch(3)
    
    assert len(batch) == 3, f"Expected 3 keys, got {len(batch)}"
    
    # Verify all keys are valid
    for i, key in enumerate(batch):
        validation = generator.validate_combsec_key(key)
        assert validation["valid"] == True, f"Batch key {i} validation failed"
    
    print(f"✅ Generated {len(batch)} valid keys")
    return True

def test_unicode_consistency():
    """Test Unicode codepoint consistency"""
    print("🔤 Testing Unicode consistency...")
    
    generator = EmojiCombsecGenerator()
    
    # Verify the globe emoji Unicode properties
    assert generator.GLOBE_EMOJI == "🌐", "Globe emoji mismatch"
    assert generator.UNICODE_CODEPOINT == "U+1F310", "Unicode codepoint mismatch"
    assert generator.HEX_VALUE == 0x1F310, "Hex value mismatch"
    assert generator.UTF8_BYTES == b'\xf0\x9f\x8c\x90', "UTF-8 bytes mismatch"
    
    print("✅ Unicode properties verified")
    return True

def test_invalid_key_handling():
    """Test handling of invalid keys"""
    print("⚠️ Testing invalid key handling...")
    
    generator = EmojiCombsecGenerator()
    
    # Test various invalid key formats
    invalid_keys = [
        "invalid-key",
        "🌐-TOOSHORT-123456-FIRM",
        "🚀-WRONGEMOJI123456-123456-FIRM",  # Wrong emoji
        "🌐-VALIDHEXKEY1234-NOTANUMBER-FIRM",  # Invalid timestamp
    ]
    
    for invalid_key in invalid_keys:
        validation = generator.validate_combsec_key(invalid_key)
        assert validation["valid"] == False, f"Invalid key incorrectly validated: {invalid_key}"
    
    print("✅ Invalid key handling works correctly")
    return True

def test_api_function_u1f310():
    """Test the standardized API function generate_combsec_key_u1f310"""
    print("🚀 Testing API function generate_combsec_key_u1f310...")
    
    # Test with default parameters (no timestamp)
    key1 = generate_combsec_key_u1f310("APIFIRM")
    
    # Test with specific timestamp
    test_timestamp = 1234567890
    key2 = generate_combsec_key_u1f310("APIFIRM", test_timestamp)
    
    # Basic format validation
    assert key1.startswith("🌐-"), f"Key 1 doesn't start with globe emoji: {key1}"
    assert key2.startswith("🌐-"), f"Key 2 doesn't start with globe emoji: {key2}"
    
    # Validate using existing validator
    generator = EmojiCombsecGenerator("APIFIRM")
    validation1 = generator.validate_combsec_key(key1)
    validation2 = generator.validate_combsec_key(key2)
    
    assert validation1["valid"] == True, "API function key 1 validation failed"
    assert validation2["valid"] == True, "API function key 2 validation failed"
    assert validation1["firm_id"] == "APIFIRM", "API function key 1 firm_id mismatch"
    assert validation2["firm_id"] == "APIFIRM", "API function key 2 firm_id mismatch"
    assert validation2["timestamp"] == test_timestamp, "API function key 2 timestamp mismatch"
    
    print(f"✅ API function test passed")
    print(f"   Key 1 (auto timestamp): {key1}")
    print(f"   Key 2 (fixed timestamp): {key2}")
    return True

def run_all_tests():
    """Run all validation tests"""
    print("🌐 ACTNEWWORLDODOR - COMBSEC Key Validation Tests")
    print("=" * 55)
    
    tests = [
        test_unicode_consistency,
        test_key_generation,
        test_key_validation,
        test_batch_generation,
        test_invalid_key_handling,
        test_api_function_u1f310,
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
    
    print("\n" + "=" * 55)
    print(f"📊 Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All tests passed! COMBSEC system is ready for deployment.")
        return True
    else:
        print("💥 Some tests failed. Please review and fix issues.")
        return False


if __name__ == "__main__":
    # Run all tests
    success = run_all_tests()
    sys.exit(0 if success else 1)
