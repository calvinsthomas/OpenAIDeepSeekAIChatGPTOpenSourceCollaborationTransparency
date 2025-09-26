#!/usr/bin/env python3
"""
QXR Bridge Integration Module

Integrates the Rust-C-Python bridge with the existing QXR social media system.
Provides high-performance processing while maintaining compatibility with the current API.
"""

import sys
import os
import time
import json
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path

# Add bridge directory to path
BRIDGE_DIR = Path(__file__).parent.parent / "rust_c_python_bridge"
sys.path.insert(0, str(BRIDGE_DIR))

# Try to import the native bridge, fall back to simulation if not available
try:
    import qxr_bridge
    BRIDGE_AVAILABLE = True
    print("🚀 Native QXR Bridge loaded successfully")
except ImportError:
    BRIDGE_AVAILABLE = False
    print("⚠️  Native bridge not available, using high-performance simulation")
    
    # Bridge simulation for development/testing
    class MockQXRBridge:
        def __init__(self):
            self.version = "QXR Bridge v0.1.0 (Simulation)"
        
        def process_data(self, data):
            if hasattr(data, 'data'):
                data = data.data
            
            base_score = data['signals'] * data['signal_strength']
            liquidity_factor = (data['max_liquidity'] ** 0.1) / 10.0
            opportunity_multiplier = 1.0 + (data['opportunities'] / 100.0)
            return base_score * liquidity_factor * opportunity_multiplier
        
        def generate_content(self, data, platform):
            if hasattr(data, 'data'):
                data = data.data
                
            score = self.process_data(data)
            
            if platform == "linkedin":
                return f"🚀 QXR Research Update: {data['signals']} signals detected with {data['signal_strength']:.3f} strength. Performance score: {score:.2f}. {data['opportunities']} opportunities identified in {data['timeframe']}."
            elif platform == "twitter":
                return f"🔥 {data['signals']} signals @ {data['signal_strength']:.3f} strength | Score: {score:.1f} | {data['opportunities']} ops | {data['timeframe']} #QXR #Trading"
            else:
                return f"QXR Analysis: {data['signals']} signals, performance {score:.2f}"
        
        def batch_process(self, data_list):
            return [self.process_data(data) for data in data_list]
        
        def version(self):
            return self.version
    
    class MockQXRResearchData:
        def __init__(self, **kwargs):
            self.data = {
                'signals': kwargs.get('signals', 0),
                'opportunities': kwargs.get('opportunities', 0),
                'signal_strength': kwargs.get('signal_strength', 0.0),
                'price_range_min': kwargs.get('price_range_min', 0.0),
                'price_range_max': kwargs.get('price_range_max', 0.0),
                'max_liquidity': kwargs.get('max_liquidity', 0),
                'strategy': kwargs.get('strategy', ''),
                'timeframe': kwargs.get('timeframe', '')
            }
    
    # Use mock classes
    qxr_bridge = type('MockModule', (), {
        'QXRBridge': MockQXRBridge,
        'QXRResearchData': MockQXRResearchData,
        'get_memory_stats': lambda: {
            'total_allocated': 0,
            'peak_allocated': 0,
            'allocation_count': 0,
            'deallocation_count': 0
        }
    })()


class QXRBridgeManager:
    """
    High-level manager for the QXR bridge integration.
    Provides a clean API for the existing QXR system while leveraging 
    the high-performance Rust-C-Python bridge.
    """
    
    def __init__(self):
        self.bridge = qxr_bridge.QXRBridge()
        self.is_native = BRIDGE_AVAILABLE
        self._stats = {
            'total_operations': 0,
            'total_processing_time': 0.0,
            'average_processing_time': 0.0
        }
    
    def get_bridge_info(self) -> Dict[str, Any]:
        """Get information about the bridge"""
        # Get version safely
        if hasattr(self.bridge, 'version'):
            if callable(self.bridge.version):
                version = self.bridge.version()
            else:
                version = self.bridge.version
        else:
            version = "Unknown"
            
        return {
            'version': version,
            'native_bridge': self.is_native,
            'performance_mode': 'Native' if self.is_native else 'Simulation',
            'stats': self._stats.copy()
        }
    
    def convert_research_data(self, research_data: Dict[str, Any]) -> Any:
        """Convert QXR research data to bridge format"""
        return qxr_bridge.QXRResearchData(
            signals=research_data.get('signals', 0),
            opportunities=research_data.get('opportunities', 0),
            signal_strength=research_data.get('signal_strength', 0.0),
            price_range_min=research_data.get('price_range', [0, 0])[0],
            price_range_max=research_data.get('price_range', [0, 0])[1] if len(research_data.get('price_range', [])) > 1 else 0,
            max_liquidity=research_data.get('max_liquidity', 0),
            strategy=research_data.get('strategy', ''),
            timeframe=research_data.get('timeframe', '')
        )
    
    def process_research_data(self, research_data: Dict[str, Any]) -> float:
        """
        Process research data with high-performance bridge
        
        Args:
            research_data: Dictionary containing research metrics
            
        Returns:
            Performance score calculated by the bridge
        """
        start_time = time.time()
        
        # Convert to bridge format
        bridge_data = self.convert_research_data(research_data)
        
        # Process with bridge
        score = self.bridge.process_data(bridge_data)
        
        # Update stats
        processing_time = time.time() - start_time
        self._stats['total_operations'] += 1
        self._stats['total_processing_time'] += processing_time
        self._stats['average_processing_time'] = (
            self._stats['total_processing_time'] / self._stats['total_operations']
        )
        
        return score
    
    def generate_social_content(self, research_data: Dict[str, Any], 
                              platforms: Optional[List[str]] = None) -> Dict[str, str]:
        """
        Generate social media content for multiple platforms
        
        Args:
            research_data: Dictionary containing research metrics
            platforms: List of platforms to generate content for
            
        Returns:
            Dictionary mapping platform names to generated content
        """
        if platforms is None:
            platforms = ['linkedin', 'twitter', 'github', 'notion']
        
        # Convert to bridge format
        bridge_data = self.convert_research_data(research_data)
        
        # Generate content for each platform
        content = {}
        for platform in platforms:
            content[platform] = self.bridge.generate_content(bridge_data, platform)
        
        return content
    
    def batch_process_research_data(self, research_data_list: List[Dict[str, Any]]) -> List[float]:
        """
        Process multiple research data items efficiently
        
        Args:
            research_data_list: List of research data dictionaries
            
        Returns:
            List of performance scores
        """
        start_time = time.time()
        
        # Convert all data to bridge format
        bridge_data_list = [self.convert_research_data(data) for data in research_data_list]
        
        # Process in batch
        scores = self.bridge.batch_process(bridge_data_list)
        
        # Update stats
        processing_time = time.time() - start_time
        self._stats['total_operations'] += len(research_data_list)
        self._stats['total_processing_time'] += processing_time
        self._stats['average_processing_time'] = (
            self._stats['total_processing_time'] / self._stats['total_operations']
        )
        
        return scores
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get memory allocation statistics from the bridge"""
        if self.is_native:
            return qxr_bridge.get_memory_stats()
        else:
            return {
                'total_allocated': 0,
                'peak_allocated': 0,
                'allocation_count': 0,
                'deallocation_count': 0,
                'note': 'Simulation mode - no actual memory tracking'
            }
    
    def optimize_for_batch_processing(self, batch_size: int = 1000) -> None:
        """Optimize bridge for batch processing scenarios"""
        # This would configure the bridge for optimal batch processing
        # In simulation mode, this is a no-op
        pass


class EnhancedSocialMediaEngine:
    """
    Enhanced Social Media Engine with Rust-C-Python bridge integration.
    Drop-in replacement for the original SocialMediaEngine with performance improvements.
    """
    
    def __init__(self, firm_id: str):
        self.firm_id = firm_id
        self.bridge_manager = QXRBridgeManager()
        
        # Try to import and extend the original engine
        try:
            from social_media_engine import SocialMediaEngine
            self.original_engine = SocialMediaEngine(firm_id)
            self.has_original = True
        except ImportError:
            self.original_engine = None
            self.has_original = False
        
        print(f"🚀 Enhanced Social Media Engine initialized for {firm_id}")
        bridge_info = self.bridge_manager.get_bridge_info()
        print(f"🔧 Bridge: {bridge_info['version']} ({bridge_info['performance_mode']})")
    
    def process_research_metrics(self, research_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process research metrics with enhanced performance
        
        Args:
            research_data: Research data dictionary
            
        Returns:
            Enhanced processing results with performance metrics
        """
        start_time = time.time()
        
        # Use bridge for high-performance processing
        performance_score = self.bridge_manager.process_research_data(research_data)
        
        # Generate enhanced content
        social_content = self.bridge_manager.generate_social_content(research_data)
        
        processing_time = time.time() - start_time
        
        return {
            'performance_score': performance_score,
            'social_content': social_content,
            'processing_time_ms': processing_time * 1000,
            'bridge_info': self.bridge_manager.get_bridge_info(),
            'original_data': research_data
        }
    
    def one_push_manual_prepare(self, research_data: Dict[str, Any], 
                               target_platforms: Optional[List[str]] = None) -> Tuple[str, Dict[str, str]]:
        """
        Enhanced one-push manual preparation with bridge acceleration
        
        Args:
            research_data: Research data dictionary
            target_platforms: List of target platforms
            
        Returns:
            Tuple of (master_file_path, posts_dict)
        """
        if target_platforms is None:
            target_platforms = ['linkedin', 'twitter', 'github', 'notion']
        
        # Process with bridge
        results = self.process_research_metrics(research_data)
        
        # Create enhanced posts
        posts = {}
        for platform in target_platforms:
            content = results['social_content'].get(platform, '')
            posts[platform] = {
                'content': content,
                'performance_score': results['performance_score'],
                'processing_time_ms': results['processing_time_ms'],
                'platform': platform,
                'generated_at': time.strftime('%Y-%m-%d %H:%M:%S'),
                'bridge_version': results['bridge_info']['version']
            }
        
        # Save to master file
        timestamp = time.strftime('%Y%m%d_%H%M%S')
        master_file = f"/tmp/qxr_bridge_posts_{timestamp}.json"
        
        master_data = {
            'metadata': {
                'firm_id': self.firm_id,
                'generated_at': time.strftime('%Y-%m-%d %H:%M:%S'),
                'bridge_info': results['bridge_info'],
                'processing_stats': {
                    'total_time_ms': results['processing_time_ms'],
                    'performance_score': results['performance_score']
                }
            },
            'research_data': research_data,
            'posts': posts
        }
        
        with open(master_file, 'w', encoding='utf-8') as f:
            json.dump(master_data, f, indent=2, default=str)
        
        return master_file, posts
    
    def get_diagnostics(self) -> Dict[str, Any]:
        """Get comprehensive diagnostics about the enhanced engine"""
        return {
            'engine_info': {
                'firm_id': self.firm_id,
                'has_original_engine': self.has_original,
                'enhanced_features': True
            },
            'bridge_info': self.bridge_manager.get_bridge_info(),
            'memory_stats': self.bridge_manager.get_memory_stats(),
            'performance_stats': self.bridge_manager._stats
        }


def demo_bridge_integration():
    """Demonstrate the bridge integration functionality"""
    print("🌐 QXR Bridge Integration Demo")
    print("=" * 60)
    
    # Create enhanced engine
    engine = EnhancedSocialMediaEngine("QXR_DEMO")
    
    # Sample research data
    research_data = {
        'signals': 45,
        'opportunities': 8,
        'signal_strength': 1.247,
        'price_range': [3420.0, 3580.0],
        'max_liquidity': 12500000,
        'strategy': 'ETH Statistical Arbitrage',
        'timeframe': '24h',
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
    }
    
    print(f"\n📊 Sample Research Data:")
    for key, value in research_data.items():
        print(f"   {key}: {value}")
    
    # Process with enhanced engine
    print(f"\n🚀 Processing with Enhanced Engine...")
    results = engine.process_research_metrics(research_data)
    
    print(f"\n📈 Results:")
    print(f"   Performance Score: {results['performance_score']:.2f}")
    print(f"   Processing Time: {results['processing_time_ms']:.2f}ms")
    print(f"   Bridge Version: {results['bridge_info']['version']}")
    
    print(f"\n📱 Generated Social Content:")
    for platform, content in results['social_content'].items():
        print(f"   {platform.upper()}:")
        print(f"      {content[:100]}...")
    
    # Test one-push preparation
    print(f"\n📦 Testing One-Push Preparation...")
    master_file, posts = engine.one_push_manual_prepare(research_data)
    
    print(f"   ✅ Master file: {master_file}")
    print(f"   📊 Generated {len(posts)} platform posts")
    
    # Show diagnostics
    print(f"\n🔍 Engine Diagnostics:")
    diagnostics = engine.get_diagnostics()
    print(f"   Bridge Mode: {diagnostics['bridge_info']['performance_mode']}")
    print(f"   Total Operations: {diagnostics['performance_stats']['total_operations']}")
    print(f"   Average Processing Time: {diagnostics['performance_stats']['average_processing_time']*1000:.2f}ms")
    
    return True


if __name__ == "__main__":
    success = demo_bridge_integration()
    print(f"\n{'🎉 Demo completed successfully!' if success else '❌ Demo failed'}")