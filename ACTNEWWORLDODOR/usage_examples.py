#!/usr/bin/env python3
"""
DISTTRANSDISSINFORCVD - Usage Examples
Practical examples for using the Distribution, Transmission, Dissemination Infrastructure
"""

from disttransdissinforcvd import PublicIPAlgorithmDistributor
import json
import time

def example_1_basic_setup():
    """Example 1: Basic system setup and partner registration"""
    print("🚀 Example 1: Basic System Setup")
    print("-" * 40)
    
    # Initialize the distribution system
    distributor = PublicIPAlgorithmDistributor(
        firm_id="YOURFIRM",
        server_host="192.168.1.10",  # Your server IP
        server_port=8080
    )
    
    # Register firm partners
    key_alpha = distributor.register_firm_partner(
        partner_id="ALPHA_TRADING",
        ip_address="192.168.1.101",
        port=8080,
        email="tech@alphatrading.com",
        priority=1  # Highest priority
    )
    
    key_beta = distributor.register_firm_partner(
        partner_id="BETA_CAPITAL",
        ip_address="192.168.1.102", 
        port=8080,
        email="systems@betacapital.com",
        priority=2
    )
    
    print(f"✅ Registered 2 firm partners")
    print(f"   - ALPHA_TRADING: {key_alpha[:20]}...")
    print(f"   - BETA_CAPITAL: {key_beta[:20]}...")
    
    return distributor

def example_2_algorithm_distribution():
    """Example 2: Algorithm distribution to all partners"""
    print("\n📦 Example 2: Algorithm Distribution")
    print("-" * 40)
    
    distributor = example_1_basic_setup()
    
    # Create a trading algorithm
    trading_algorithm = {
        "strategy_type": "momentum_trading",
        "parameters": {
            "lookback_period": 20,
            "momentum_threshold": 0.02,
            "risk_limit": 0.05,
            "position_size": 0.1
        },
        "entry_conditions": [
            "price > sma_20",
            "momentum > threshold",
            "risk_score < limit"
        ],
        "exit_conditions": [
            "profit_target_reached",
            "stop_loss_triggered",
            "momentum_reversal"
        ],
        "code_snippet": """
def calculate_momentum(prices, period=20):
    return (prices[-1] / prices[-period]) - 1

def should_enter_trade(price, sma, momentum, threshold):
    return price > sma and momentum > threshold
        """
    }
    
    # Package the algorithm
    algorithm_package = distributor.create_algorithm_package(
        algorithm_name="MomentumTradingStrategy",
        algorithm_data=trading_algorithm,
        version="2.1.3",
        is_urgent=False
    )
    
    print(f"📋 Created algorithm package:")
    print(f"   - Name: {algorithm_package['algorithm_name']}")
    print(f"   - Version: {algorithm_package['version']}")
    print(f"   - Package ID: {algorithm_package['package_id']}")
    print(f"   - COMBSEC Key: {algorithm_package['combsec_key'][:30]}...")
    
    # Distribute to all partners
    distribution_results = distributor.distribute_algorithm_instant(algorithm_package)
    
    print(f"📊 Distribution Results:")
    print(f"   - Total Partners: {distribution_results['total_partners']}")
    print(f"   - Successful: {distribution_results['successful_transmissions']}")
    print(f"   - Failed: {distribution_results['failed_transmissions']}")
    
    return distributor, algorithm_package

def example_3_urgent_updates():
    """Example 3: Urgent update distribution"""
    print("\n🚨 Example 3: Urgent Update Distribution")
    print("-" * 40)
    
    distributor = example_1_basic_setup()
    
    # Critical market update
    urgent_data = {
        "alert_type": "MARKET_VOLATILITY",
        "severity": "CRITICAL",
        "market": "US_EQUITIES",
        "volatility_spike": 0.35,
        "recommended_actions": [
            "Reduce position sizes by 50%",
            "Increase stop-loss tightness",
            "Pause new entry signals",
            "Monitor VIX levels closely"
        ],
        "updated_risk_parameters": {
            "max_position_size": 0.05,  # Reduced from 0.1
            "stop_loss_distance": 0.02,  # Tightened from 0.03
            "correlation_limit": 0.3     # Reduced from 0.5
        }
    }
    
    # Send urgent update
    urgent_results = distributor.send_urgent_update(
        update_message="CRITICAL: Market volatility spike detected. Immediate action required.",
        algorithm_data=urgent_data,
        priority=1
    )
    
    print(f"⚡ Urgent Update Sent:")
    print(f"   - Partners Notified: {urgent_results['total_partners']}")
    print(f"   - Successful Deliveries: {urgent_results['successful_transmissions']}")
    print(f"   - Package ID: {urgent_results['package_id']}")
    
    # Check system status after urgent update
    status = distributor.get_distribution_status()
    print(f"   - Urgent Updates Queued: {status['urgent_updates_queued']}")
    
    return distributor

def example_4_batch_operations():
    """Example 4: Batch algorithm distribution"""
    print("\n🔄 Example 4: Batch Algorithm Distribution")
    print("-" * 40)
    
    distributor = example_1_basic_setup()
    
    # Multiple algorithms to distribute
    algorithms = [
        {
            "name": "RiskManagementAlgorithm",
            "data": {
                "risk_model": "VaR_95",
                "calculation_method": "historical_simulation",
                "lookback_days": 252
            },
            "version": "1.5.2"
        },
        {
            "name": "PortfolioOptimizer",
            "data": {
                "optimization_method": "mean_variance",
                "constraints": {"max_weight": 0.1, "min_weight": 0.01},
                "rebalance_frequency": "weekly"
            },
            "version": "3.0.1"
        },
        {
            "name": "SignalAggregator",
            "data": {
                "signal_sources": ["technical", "fundamental", "sentiment"],
                "weighting_scheme": "equal_weight",
                "threshold": 0.6
            },
            "version": "2.2.0"  
        }
    ]
    
    distribution_results = []
    
    for algo in algorithms:
        # Create package
        package = distributor.create_algorithm_package(
            algorithm_name=algo["name"],
            algorithm_data=algo["data"],
            version=algo["version"]
        )
        
        # Distribute
        result = distributor.distribute_algorithm_instant(package)
        distribution_results.append(result)
        
        print(f"📦 Distributed {algo['name']} v{algo['version']}")
        
    # Summary
    total_distributions = len(distribution_results)
    total_successful = sum(r['successful_transmissions'] for r in distribution_results)
    total_failed = sum(r['failed_transmissions'] for r in distribution_results)
    
    print(f"📊 Batch Distribution Summary:")
    print(f"   - Total Algorithms: {total_distributions}")
    print(f"   - Total Successful Transmissions: {total_successful}")
    print(f"   - Total Failed Transmissions: {total_failed}")
    
    return distributor

def example_5_monitoring_and_status():
    """Example 5: System monitoring and status reporting"""
    print("\n📈 Example 5: System Monitoring and Status")
    print("-" * 40)
    
    distributor = example_1_basic_setup()
    
    # Add more partners for demonstration
    distributor.register_firm_partner("GAMMA_FUNDS", "192.168.1.103", priority=1)
    distributor.register_firm_partner("DELTA_INVESTMENTS", "192.168.1.104", priority=3)
    
    # Get system status
    status = distributor.get_distribution_status()
    
    print(f"🔍 System Status Report:")
    print(f"   - Firm ID: {status['firm_id']}")
    print(f"   - Server Connected: {status['server_connected']}")
    print(f"   - Total Partners: {status['total_partners']}")
    print(f"   - Active Partners: {status['active_partners']}")
    print(f"   - COMBSEC System: {status['combsec_system']}")
    print(f"   - Registered Partners: {', '.join(status['partners'])}")
    
    # Export partner registry for backup
    registry_export = distributor.export_partner_registry()
    
    print(f"\n💾 Partner Registry Export:")
    print(f"   - Export Timestamp: {registry_export['export_timestamp']}")
    print(f"   - Total Partners in Export: {registry_export['total_partners']}")
    
    # Display partner details (without sensitive data)
    for partner_id, partner_data in registry_export['partners'].items():
        print(f"   - {partner_id}: {partner_data['ip_address']} (Priority: {partner_data['priority']})")
    
    return distributor

def example_6_server_connection():
    """Example 6: Server connection and management"""
    print("\n🔗 Example 6: Server Connection Management")
    print("-" * 40)
    
    # Try different server configurations
    servers = [
        {"host": "localhost", "port": 8080, "name": "Local Development"},
        {"host": "192.168.1.10", "port": 8080, "name": "Internal Server"},
        {"host": "10.0.0.100", "port": 9090, "name": "Production Server"}
    ]
    
    for server in servers:
        print(f"\n🔌 Attempting connection to {server['name']}...")
        
        distributor = PublicIPAlgorithmDistributor(
            firm_id="YOURFIRM",
            server_host=server["host"],
            server_port=server["port"]
        )
        
        # Attempt connection
        connection_result = distributor.connect_to_server()
        
        print(f"   - Host: {server['host']}:{server['port']}")
        print(f"   - Connected: {connection_result['connected']}")
        
        if connection_result['connected']:
            print(f"   - Connection Time: {connection_result['connection_time']}")
            print(f"   - Server Response: {connection_result.get('server_response', 'N/A')}")
        else:
            print(f"   - Error: {connection_result.get('error', 'Unknown error')}")
    
    print(f"\n📚 See 'connect_to_server_documentation.md' for full server setup instructions")

def run_all_examples():
    """Run all usage examples"""
    print("🌐 DISTTRANSDISSINFORCVD - Usage Examples")
    print("=" * 60)
    print("Demonstrating the Distribution, Transmission, Dissemination Infrastructure")
    print("for instant algorithm distribution to all firm partners.")
    print()
    
    try:
        example_1_basic_setup()
        example_2_algorithm_distribution()
        example_3_urgent_updates()
        example_4_batch_operations()
        example_5_monitoring_and_status()
        example_6_server_connection()
        
        print("\n" + "=" * 60)
        print("🎉 All examples completed successfully!")
        print("📖 For more information, see:")
        print("   - connect_to_server_documentation.md")
        print("   - COMBSEC_KEY_TECH_DESIGN_DOC_U1F310.md")
        print("   - integration_protocols.md")
        
    except Exception as e:
        print(f"\n❌ Example execution failed: {str(e)}")
        print("💡 Note: Some failures are expected without actual server infrastructure")

if __name__ == "__main__":
    run_all_examples()