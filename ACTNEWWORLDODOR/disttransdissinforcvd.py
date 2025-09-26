#!/usr/bin/env python3
"""
DISTTRANSDISSINFORCVD - Distribution, Transmission, Dissemination Infrastructure for CVD
Public IP Algorithm Distribution System for Instant Firm Partner Communication

This module provides instant distribution, dissemination, and transmission capabilities
for algorithms and urgent updates to all firm partners.
"""

import socket
import json
import time
import threading
from typing import List, Dict, Optional, Any
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import hashlib
import logging

# Import existing COMBSEC system
from emoji_combsec_generator import EmojiCombsecGenerator

class PublicIPAlgorithmDistributor:
    """
    Main class for distributing algorithms and updates to firm partners
    via public IP infrastructure with instant transmission capabilities.
    """
    
    def __init__(self, firm_id: str = "YOURFIRM", 
                 server_host: str = "localhost", 
                 server_port: int = 8080):
        """
        Initialize the distribution system
        
        Args:
            firm_id: Unique identifier for the firm
            server_host: Server host for connections
            server_port: Server port for connections
        """
        self.firm_id = firm_id
        self.server_host = server_host
        self.server_port = server_port
        
        # Initialize COMBSEC key generator for secure transmission
        self.combsec_generator = EmojiCombsecGenerator(firm_id)
        
        # Firm partner registry
        self.firm_partners = {}
        self.urgent_update_queue = []
        
        # Logging setup
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Server connection status
        self.server_connected = False
        
    def register_firm_partner(self, partner_id: str, 
                            ip_address: str, 
                            port: int = 8080,
                            email: Optional[str] = None,
                            priority: int = 1):
        """
        Register a firm partner for algorithm distribution
        
        Args:
            partner_id: Unique partner identifier
            ip_address: Partner's public IP address
            port: Communication port
            email: Optional email for notifications
            priority: Priority level (1=highest, 5=lowest)
        """
        partner_key = self.combsec_generator.generate_combsec_key()
        
        self.firm_partners[partner_id] = {
            "id": partner_id,
            "ip_address": ip_address,
            "port": port,
            "email": email,
            "priority": priority,
            "combsec_key": partner_key,
            "last_contact": None,
            "status": "registered",
            "algorithms_received": []
        }
        
        self.logger.info(f"Registered firm partner: {partner_id} at {ip_address}:{port}")
        return partner_key
    
    def create_algorithm_package(self, algorithm_name: str, 
                               algorithm_data: Any,
                               version: str = "1.0",
                               is_urgent: bool = False) -> Dict[str, Any]:
        """
        Create a standardized algorithm package for distribution
        
        Args:
            algorithm_name: Name of the algorithm
            algorithm_data: Algorithm code, parameters, or data
            version: Algorithm version
            is_urgent: Mark as urgent update
            
        Returns:
            Formatted algorithm package
        """
        timestamp = int(time.time())
        package_id = hashlib.sha256(
            f"{algorithm_name}{version}{timestamp}".encode()
        ).hexdigest()[:16]
        
        package = {
            "package_id": package_id,
            "algorithm_name": algorithm_name,
            "algorithm_data": algorithm_data,
            "version": version,
            "firm_id": self.firm_id,
            "timestamp": timestamp,
            "datetime": datetime.fromtimestamp(timestamp).isoformat(),
            "is_urgent": is_urgent,
            "combsec_key": self.combsec_generator.generate_combsec_key(),
            "distribution_type": "DISTTRANSDISSINFORCVD",
            "checksum": hashlib.md5(str(algorithm_data).encode()).hexdigest()
        }
        
        return package
    
    def distribute_algorithm_instant(self, algorithm_package: Dict[str, Any],
                                   target_partners: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Instantly distribute algorithm to all or specified firm partners
        
        Args:
            algorithm_package: Algorithm package to distribute
            target_partners: Optional list of specific partner IDs
            
        Returns:
            Distribution results
        """
        if target_partners is None:
            target_partners = list(self.firm_partners.keys())
        
        distribution_results = {
            "package_id": algorithm_package["package_id"],
            "distribution_timestamp": datetime.now().isoformat(),
            "total_partners": len(target_partners),
            "successful_transmissions": 0,
            "failed_transmissions": 0,
            "partner_results": {}
        }
        
        # Sort partners by priority for urgent updates
        if algorithm_package["is_urgent"]:
            sorted_partners = sorted(
                target_partners,
                key=lambda p: self.firm_partners[p]["priority"]
            )
        else:
            sorted_partners = target_partners
        
        # Distribute to each partner
        for partner_id in sorted_partners:
            try:
                result = self._transmit_to_partner(partner_id, algorithm_package)
                distribution_results["partner_results"][partner_id] = result
                
                if result["success"]:
                    distribution_results["successful_transmissions"] += 1
                else:
                    distribution_results["failed_transmissions"] += 1
                    
            except Exception as e:
                self.logger.error(f"Failed to transmit to {partner_id}: {str(e)}")
                distribution_results["partner_results"][partner_id] = {
                    "success": False,
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                }
                distribution_results["failed_transmissions"] += 1
        
        self.logger.info(
            f"Distribution complete: {distribution_results['successful_transmissions']}"
            f"/{distribution_results['total_partners']} successful"
        )
        
        return distribution_results
    
    def _transmit_to_partner(self, partner_id: str, 
                           algorithm_package: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transmit algorithm package to specific partner via TCP/IP
        
        Args:
            partner_id: Target partner ID
            algorithm_package: Package to transmit
            
        Returns:
            Transmission result
        """
        if partner_id not in self.firm_partners:
            raise ValueError(f"Partner {partner_id} not registered")
        
        partner = self.firm_partners[partner_id]
        
        try:
            # Create socket connection
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(10)  # 10 second timeout
                
                # Attempt connection to partner
                sock.connect((partner["ip_address"], partner["port"]))
                
                # Prepare transmission data
                transmission_data = {
                    "type": "ALGORITHM_DISTRIBUTION",
                    "source_firm": self.firm_id,
                    "target_partner": partner_id,
                    "combsec_verification": partner["combsec_key"],
                    "package": algorithm_package,
                    "transmission_time": datetime.now().isoformat()
                }
                
                # Send data
                message = json.dumps(transmission_data).encode('utf-8')
                sock.sendall(message)
                
                # Wait for acknowledgment
                response = sock.recv(1024).decode('utf-8')
                response_data = json.loads(response)
                
                # Update partner status
                partner["last_contact"] = datetime.now().isoformat()
                partner["status"] = "active"
                partner["algorithms_received"].append(algorithm_package["package_id"])
                
                return {
                    "success": True,
                    "partner_id": partner_id,
                    "transmission_time": datetime.now().isoformat(),
                    "response": response_data,
                    "bytes_sent": len(message)
                }
                
        except Exception as e:
            partner["status"] = "connection_failed"
            return {
                "success": False,
                "partner_id": partner_id,
                "error": str(e),
                "transmission_time": datetime.now().isoformat()
            }
    
    def send_urgent_update(self, update_message: str, 
                          algorithm_data: Optional[Any] = None,
                          priority: int = 1) -> Dict[str, Any]:
        """
        Send urgent update to all firm partners with highest priority
        
        Args:
            update_message: Urgent message content
            algorithm_data: Optional algorithm or data update
            priority: Update priority (1=critical, 5=low)
            
        Returns:
            Urgent update distribution results
        """
        urgent_package = self.create_algorithm_package(
            algorithm_name="URGENT_UPDATE",
            algorithm_data={
                "message": update_message,
                "data": algorithm_data,
                "priority": priority
            },
            version=f"urgent_{int(time.time())}",
            is_urgent=True
        )
        
        # Add to urgent queue
        self.urgent_update_queue.append(urgent_package)
        
        # Distribute immediately
        results = self.distribute_algorithm_instant(urgent_package)
        
        # Send email notifications if configured
        self._send_urgent_email_notifications(update_message, results)
        
        return results
    
    def _send_urgent_email_notifications(self, message: str, 
                                       distribution_results: Dict[str, Any]):
        """
        Send email notifications for urgent updates
        
        Args:
            message: Urgent message
            distribution_results: Distribution results
        """
        partners_with_email = [
            p for p in self.firm_partners.values() 
            if p.get("email")
        ]
        
        for partner in partners_with_email:
            try:
                # This would normally connect to SMTP server
                # For now, just log the notification
                self.logger.info(
                    f"Email notification sent to {partner['email']}: {message}"
                )
            except Exception as e:
                self.logger.error(f"Failed to send email to {partner['email']}: {e}")
    
    def connect_to_server(self) -> Dict[str, Any]:
        """
        Connect to the main server infrastructure
        See documentation in "CONNECT TO SERVER" section
        
        Returns:
            Connection status and server information
        """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(5)
                sock.connect((self.server_host, self.server_port))
                
                # Send connection request with COMBSEC authentication
                auth_data = {
                    "type": "SERVER_CONNECTION_REQUEST",
                    "firm_id": self.firm_id,
                    "combsec_key": self.combsec_generator.generate_combsec_key(),
                    "timestamp": datetime.now().isoformat(),
                    "capabilities": ["ALGORITHM_DISTRIBUTION", "URGENT_UPDATES"]
                }
                
                message = json.dumps(auth_data).encode('utf-8')
                sock.sendall(message)
                
                response = sock.recv(1024).decode('utf-8')
                server_response = json.loads(response)
                
                self.server_connected = True
                
                return {
                    "connected": True,
                    "server_host": self.server_host,
                    "server_port": self.server_port,
                    "connection_time": datetime.now().isoformat(),
                    "server_response": server_response
                }
                
        except Exception as e:
            self.server_connected = False
            return {
                "connected": False,
                "error": str(e),
                "connection_attempt_time": datetime.now().isoformat()
            }
    
    def get_distribution_status(self) -> Dict[str, Any]:
        """
        Get current status of the distribution system
        
        Returns:
            System status information
        """
        return {
            "firm_id": self.firm_id,
            "server_connected": self.server_connected,
            "total_partners": len(self.firm_partners),
            "active_partners": len([
                p for p in self.firm_partners.values() 
                if p["status"] == "active"
            ]),
            "urgent_updates_queued": len(self.urgent_update_queue),
            "system_timestamp": datetime.now().isoformat(),
            "combsec_system": "ACTIVE",
            "partners": list(self.firm_partners.keys())
        }
    
    def export_partner_registry(self) -> Dict[str, Any]:
        """
        Export partner registry for backup or transfer
        
        Returns:
            Partner registry data
        """
        return {
            "firm_id": self.firm_id,
            "export_timestamp": datetime.now().isoformat(),
            "total_partners": len(self.firm_partners),
            "partners": {
                pid: {
                    **partner_data,
                    "combsec_key": "REDACTED_FOR_SECURITY"
                }
                for pid, partner_data in self.firm_partners.items()
            }
        }


def demo_disttransdissinforcvd():
    """
    Demonstration of the DISTTRANSDISSINFORCVD system
    """
    print("🌐 DISTTRANSDISSINFORCVD - Distribution System Demo")
    print("=" * 60)
    
    # Initialize distributor
    distributor = PublicIPAlgorithmDistributor("DEMOFIRM")
    
    # Register some demo partners
    distributor.register_firm_partner("PARTNER_A", "192.168.1.100", email="partner.a@firm.com")
    distributor.register_firm_partner("PARTNER_B", "192.168.1.101", email="partner.b@firm.com")
    distributor.register_firm_partner("PARTNER_C", "192.168.1.102", priority=2)
    
    print(f"✅ Registered {len(distributor.firm_partners)} firm partners")
    
    # Create algorithm package
    algorithm_data = {
        "algorithm_type": "trading_strategy",
        "parameters": {"risk_level": 0.05, "time_horizon": "1D"},
        "code": "def calculate_risk(): return 0.05"
    }
    
    package = distributor.create_algorithm_package(
        "RiskCalculationAlgorithm",
        algorithm_data,
        version="2.1.0"
    )
    
    print(f"📦 Created algorithm package: {package['package_id']}")
    
    # Send urgent update (simulated - won't actually connect)
    print("\n🚨 Sending urgent update...")
    urgent_results = distributor.send_urgent_update(
        "CRITICAL: New risk parameters deployed. Update immediately.",
        algorithm_data,
        priority=1
    )
    
    print(f"📊 Urgent update results: {urgent_results['total_partners']} partners targeted")
    
    # Show system status
    status = distributor.get_distribution_status()
    print(f"\n📈 System Status:")
    print(f"   - Firm ID: {status['firm_id']}")
    print(f"   - Total Partners: {status['total_partners']}")
    print(f"   - Urgent Updates Queued: {status['urgent_updates_queued']}")
    print(f"   - COMBSEC System: {status['combsec_system']}")
    
    return distributor


if __name__ == "__main__":
    # Run demonstration
    demo_distributor = demo_disttransdissinforcvd()
    
    # Try server connection (will fail but demonstrate functionality)
    print("\n🔗 Testing server connection...")
    connection_result = demo_distributor.connect_to_server()
    print(f"Connection result: {connection_result['connected']}")
    if not connection_result['connected']:
        print(f"Note: Connection failed as expected - no server running: {connection_result.get('error', 'Unknown error')}")