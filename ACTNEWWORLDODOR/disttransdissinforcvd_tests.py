#!/usr/bin/env python3
"""
DISTTRANSDISSINFORCVD - Comprehensive Test Suite
Tests for the Distribution, Transmission, Dissemination Infrastructure
"""

import sys
import os
import json
import time
from datetime import datetime

# Add the ACTNEWWORLDODOR directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from disttransdissinforcvd import PublicIPAlgorithmDistributor

def test_distributor_initialization():
    """Test basic distributor initialization"""
    print("🔧 Testing distributor initialization...")
    
    distributor = PublicIPAlgorithmDistributor("TESTFIRM")
    
    assert distributor.firm_id == "TESTFIRM", "Firm ID not set correctly"
    assert distributor.server_host == "localhost", "Default server host incorrect"
    assert distributor.server_port == 8080, "Default server port incorrect"
    assert len(distributor.firm_partners) == 0, "Should start with no partners"
    assert len(distributor.urgent_update_queue) == 0, "Should start with empty urgent queue"
    
    print("✅ Distributor initialization successful")
    return True

def test_firm_partner_registration():
    """Test firm partner registration functionality"""
    print("👥 Testing firm partner registration...")
    
    distributor = PublicIPAlgorithmDistributor("TESTFIRM")
    
    # Register a partner
    partner_key = distributor.register_firm_partner(
        "PARTNER_TEST",
        "192.168.1.100",
        port=8080,
        email="test@partner.com",
        priority=1
    )
    
    assert len(distributor.firm_partners) == 1, "Partner not registered"
    assert "PARTNER_TEST" in distributor.firm_partners, "Partner ID not found"
    
    partner = distributor.firm_partners["PARTNER_TEST"]
    assert partner["ip_address"] == "192.168.1.100", "IP address not set correctly"
    assert partner["email"] == "test@partner.com", "Email not set correctly"
    assert partner["priority"] == 1, "Priority not set correctly"
    assert partner["status"] == "registered", "Status not set correctly"
    assert partner_key.startswith("🌐-"), "COMBSEC key format invalid"
    
    print("✅ Firm partner registration successful")
    return True

def test_algorithm_package_creation():
    """Test algorithm package creation"""
    print("📦 Testing algorithm package creation...")
    
    distributor = PublicIPAlgorithmDistributor("TESTFIRM")
    
    algorithm_data = {
        "strategy": "test_strategy",
        "parameters": {"risk": 0.05},
        "code": "def test(): return True"
    }
    
    package = distributor.create_algorithm_package(
        "TestAlgorithm",
        algorithm_data,
        version="1.0.0",
        is_urgent=False
    )
    
    # Validate package structure
    required_fields = [
        "package_id", "algorithm_name", "algorithm_data", "version",
        "firm_id", "timestamp", "datetime", "is_urgent",
        "combsec_key", "distribution_type", "checksum"
    ]
    
    for field in required_fields:
        assert field in package, f"Package missing required field: {field}"
    
    assert package["algorithm_name"] == "TestAlgorithm", "Algorithm name incorrect"
    assert package["version"] == "1.0.0", "Version incorrect"
    assert package["firm_id"] == "TESTFIRM", "Firm ID incorrect"
    assert package["is_urgent"] == False, "Urgent flag incorrect"
    assert package["distribution_type"] == "DISTTRANSDISSINFORCVD", "Distribution type incorrect"
    assert len(package["package_id"]) == 16, "Package ID length incorrect"
    assert package["combsec_key"].startswith("🌐-"), "COMBSEC key format invalid"
    
    print("✅ Algorithm package creation successful")
    return True

def test_urgent_update_creation():
    """Test urgent update functionality"""
    print("🚨 Testing urgent update creation...")
    
    distributor = PublicIPAlgorithmDistributor("TESTFIRM")
    
    # Register partners first
    distributor.register_firm_partner("URGENT_TEST_1", "192.168.1.101", priority=1)
    distributor.register_firm_partner("URGENT_TEST_2", "192.168.1.102", priority=2)
    
    # Create urgent update (will fail transmission but test package creation)
    update_message = "CRITICAL: Test urgent update message"
    algorithm_data = {"update_type": "critical", "data": "test_data"}
    
    try:
        results = distributor.send_urgent_update(
            update_message,
            algorithm_data,
            priority=1
        )
        
        # Validate results structure
        assert "package_id" in results, "Results missing package_id"
        assert "total_partners" in results, "Results missing total_partners"
        assert results["total_partners"] == 2, "Wrong number of partners targeted"
        
        # Check urgent queue
        assert len(distributor.urgent_update_queue) == 1, "Urgent update not queued"
        
        urgent_package = distributor.urgent_update_queue[0]
        assert urgent_package["is_urgent"] == True, "Package not marked as urgent"
        assert urgent_package["algorithm_name"] == "URGENT_UPDATE", "Wrong algorithm name"
        
        print("✅ Urgent update creation successful")
        return True
        
    except Exception as e:
        # Expected to fail on actual transmission
        if "connection" in str(e).lower() or "refused" in str(e).lower():
            print("✅ Urgent update creation successful (transmission failed as expected)")
            return True
        else:
            raise e

def test_system_status():
    """Test system status reporting"""
    print("📊 Testing system status reporting...")
    
    distributor = PublicIPAlgorithmDistributor("TESTFIRM")
    
    # Register some partners
    distributor.register_firm_partner("STATUS_TEST_1", "192.168.1.101")
    distributor.register_firm_partner("STATUS_TEST_2", "192.168.1.102")
    
    status = distributor.get_distribution_status()
    
    # Validate status structure
    required_status_fields = [
        "firm_id", "server_connected", "total_partners", "active_partners",
        "urgent_updates_queued", "system_timestamp", "combsec_system", "partners"
    ]
    
    for field in required_status_fields:
        assert field in status, f"Status missing required field: {field}"
    
    assert status["firm_id"] == "TESTFIRM", "Firm ID incorrect in status"
    assert status["total_partners"] == 2, "Total partners count incorrect"
    assert status["combsec_system"] == "ACTIVE", "COMBSEC system status incorrect"
    assert isinstance(status["partners"], list), "Partners should be a list"
    assert len(status["partners"]) == 2, "Partners list length incorrect"
    
    print("✅ System status reporting successful")
    return True

def test_partner_registry_export():
    """Test partner registry export functionality"""
    print("💾 Testing partner registry export...")
    
    distributor = PublicIPAlgorithmDistributor("TESTFIRM")
    
    # Register partners with different configurations
    distributor.register_firm_partner(
        "EXPORT_TEST_1", 
        "192.168.1.101", 
        email="export1@test.com",
        priority=1
    )
    distributor.register_firm_partner(
        "EXPORT_TEST_2", 
        "192.168.1.102", 
        priority=3
    )
    
    export_data = distributor.export_partner_registry()
    
    # Validate export structure
    assert "firm_id" in export_data, "Export missing firm_id"
    assert "export_timestamp" in export_data, "Export missing timestamp"
    assert "total_partners" in export_data, "Export missing total_partners"
    assert "partners" in export_data, "Export missing partners data"
    
    assert export_data["firm_id"] == "TESTFIRM", "Firm ID incorrect in export"
    assert export_data["total_partners"] == 2, "Total partners count incorrect in export"
    
    # Check partner data
    partners_data = export_data["partners"]
    assert "EXPORT_TEST_1" in partners_data, "Partner 1 not in export"
    assert "EXPORT_TEST_2" in partners_data, "Partner 2 not in export"
    
    # Verify security - COMBSEC keys should be redacted
    for partner_id, partner_data in partners_data.items():
        assert partner_data["combsec_key"] == "REDACTED_FOR_SECURITY", \
            f"COMBSEC key not redacted for {partner_id}"
    
    print("✅ Partner registry export successful")
    return True

def test_server_connection_attempt():
    """Test server connection functionality (will fail but test structure)"""
    print("🔗 Testing server connection attempt...")
    
    distributor = PublicIPAlgorithmDistributor("TESTFIRM", "localhost", 8080)
    
    # Attempt connection (expected to fail)
    connection_result = distributor.connect_to_server()
    
    # Validate connection result structure
    assert "connected" in connection_result, "Connection result missing 'connected' field"
    assert isinstance(connection_result["connected"], bool), "Connected field should be boolean"
    
    if connection_result["connected"]:
        # If somehow connected, validate success structure
        required_success_fields = [
            "server_host", "server_port", "connection_time", "server_response"
        ]
        for field in required_success_fields:
            assert field in connection_result, f"Success result missing {field}"
    else:
        # Expected failure case
        assert "error" in connection_result, "Failure result missing error field"
        assert "connection_attempt_time" in connection_result, "Missing attempt time"
    
    print("✅ Server connection attempt successful (failed as expected)")
    return True

def test_combsec_integration():
    """Test integration with existing COMBSEC system"""
    print("🔐 Testing COMBSEC integration...")
    
    distributor = PublicIPAlgorithmDistributor("TESTFIRM")
    
    # Test COMBSEC generator initialization
    assert distributor.combsec_generator is not None, "COMBSEC generator not initialized"
    assert distributor.combsec_generator.firm_id == "TESTFIRM", "COMBSEC firm ID mismatch"
    
    # Test key generation
    test_key = distributor.combsec_generator.generate_combsec_key()
    validation = distributor.combsec_generator.validate_combsec_key(test_key)
    
    assert validation["valid"] == True, "Generated COMBSEC key validation failed"
    assert validation["firm_id"] == "TESTFIRM", "COMBSEC key firm ID mismatch"
    assert validation["emoji"] == "🌐", "COMBSEC key emoji mismatch"
    
    print("✅ COMBSEC integration successful")
    return True

def test_demo_functionality():
    """Test the demo function"""
    print("🎭 Testing demo functionality...")
    
    try:
        from disttransdissinforcvd import demo_disttransdissinforcvd
        
        # Run demo (should not crash)
        demo_distributor = demo_disttransdissinforcvd()
        
        # Validate demo results
        assert demo_distributor is not None, "Demo distributor not returned"
        assert len(demo_distributor.firm_partners) == 3, "Demo should register 3 partners"
        assert demo_distributor.firm_id == "DEMOFIRM", "Demo firm ID incorrect"
        
        print("✅ Demo functionality successful")
        return True
        
    except Exception as e:
        print(f"❌ Demo functionality failed: {str(e)}")
        return False

def run_all_disttransdissinforcvd_tests():
    """Run all DISTTRANSDISSINFORCVD tests"""
    print("🌐 DISTTRANSDISSINFORCVD - Distribution System Test Suite")
    print("=" * 70)
    
    tests = [
        test_distributor_initialization,
        test_firm_partner_registration,
        test_algorithm_package_creation,
        test_urgent_update_creation,
        test_system_status,
        test_partner_registry_export,
        test_server_connection_attempt,
        test_combsec_integration,
        test_demo_functionality,
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
    
    print("\n" + "=" * 70)
    print(f"📊 Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All DISTTRANSDISSINFORCVD tests passed! System ready for deployment.")
        return True
    else:
        print("💥 Some tests failed. Please review and fix issues.")
        return False

if __name__ == "__main__":
    # Run all tests
    success = run_all_disttransdissinforcvd_tests()
    sys.exit(0 if success else 1)