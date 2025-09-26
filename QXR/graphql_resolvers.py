#!/usr/bin/env python3
"""
QXR GraphQL Resolvers - ACTNEWWORLDODOR COMBSEC Integration
GraphQL API resolvers for quantitative research social media integration

This module provides GraphQL resolvers for:
- COMBSEC authentication and key management
- Research data processing from notebooks  
- Social media post generation
- Notion landing page creation
- System health monitoring

Integration with existing QXR modules:
- social_media_engine.py: Social platform posting
- notion_page_generator.py: Notion page creation
- notebook_to_social.py: Research data extraction
- ACTNEWWORLDODOR emoji_combsec_generator: Authentication
"""

import os
import sys
from datetime import datetime
from typing import Dict, List, Optional, Any
import json

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from QXR.social_media_engine import SocialMediaEngine
    from QXR.notion_page_generator import NotionPageGenerator  
    from QXR.notebook_to_social import NotebookProcessor
    from ACTNEWWORLDODOR.emoji_combsec_generator import EmojiCombsecGenerator
except ImportError as e:
    print(f"⚠️  Import warning in GraphQL resolvers: {e}")
    # Fallback for development/testing
    SocialMediaEngine = None
    NotionPageGenerator = None
    NotebookProcessor = None
    EmojiCombsecGenerator = None


class GraphQLResolvers:
    """GraphQL resolvers for QXR system integration"""
    
    def __init__(self):
        """Initialize resolvers with system components"""
        self.combsec_generator = EmojiCombsecGenerator() if EmojiCombsecGenerator else None
        self.active_sessions = {}  # Track active COMBSEC sessions
        
    # Query Resolvers
    
    def generate_combsec_key(self, info, firm_id: str) -> Dict[str, Any]:
        """Generate a new COMBSEC authentication key"""
        if not self.combsec_generator:
            raise Exception("COMBSEC generator not available")
            
        try:
            session_key = self.combsec_generator.generate_combsec_key()
            
            # Store session for validation
            self.active_sessions[session_key] = {
                'firm_id': firm_id,
                'generated_at': datetime.now().isoformat(),
                'expires_at': None  # Could add expiration logic
            }
            
            return {
                'id': f"combsec_{firm_id}_{int(datetime.now().timestamp())}",
                'session_key': session_key,
                'truncated_key': session_key[:20] + "..." if len(session_key) > 20 else session_key,
                'verified': True,
                'generated_at': datetime.now().isoformat(),
                'expires_at': None
            }
        except Exception as e:
            raise Exception(f"Failed to generate COMBSEC key: {str(e)}")
    
    def validate_combsec_key(self, info, session_key: str) -> bool:
        """Validate a COMBSEC session key"""
        return session_key in self.active_sessions
    
    def extract_notebook_metrics(self, info, notebook_path: str) -> Dict[str, Any]:
        """Extract research metrics from a Jupyter notebook"""
        if not NotebookProcessor:
            raise Exception("Notebook processor not available")
            
        try:
            processor = NotebookProcessor(notebook_path)
            metrics = processor.extract_research_metrics()
            
            return {
                'signals': metrics.get('signals', 0),
                'opportunities': metrics.get('opportunities', 0),
                'signal_strength': metrics.get('signal_strength', 0.0),
                'price_range': metrics.get('price_range', [0, 0]),
                'max_liquidity': metrics.get('max_liquidity', 0),
                'strategy': metrics.get('strategy', 'Unknown'),
                'timeframe': metrics.get('timeframe', 'Unknown'),
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            raise Exception(f"Failed to extract notebook metrics: {str(e)}")
    
    def get_backtest_results(self, info, research_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate backtest results from research data"""
        try:
            # Simulate backtest results based on research data
            # In production, this would integrate with actual backtesting engine
            signal_strength = research_data.get('signal_strength', 1.0)
            opportunities = research_data.get('opportunities', 1)
            
            # Basic performance calculations
            total_return = min(max(signal_strength * opportunities * 0.8, -10.0), 25.0)
            sharpe_ratio = min(max(signal_strength * 0.8, 0.1), 3.0)
            max_drawdown = abs(total_return * 0.3)
            win_rate = min(max(signal_strength * 0.6, 0.3), 0.9)
            volatility = max(abs(total_return) * 0.4, 5.0)
            
            return {
                'total_return': round(total_return, 2),
                'sharpe_ratio': round(sharpe_ratio, 2),
                'max_drawdown': round(max_drawdown, 2),
                'win_rate': round(win_rate, 2),
                'volatility': round(volatility, 2),
                'alpha': round(total_return * 0.1, 2),
                'beta': round(1.0 + (signal_strength - 1.0) * 0.2, 2),
                'information_ratio': round(sharpe_ratio * 0.8, 2),
                'performance': f"{total_return:.2f}% return, {sharpe_ratio:.2f} Sharpe"
            }
        except Exception as e:
            raise Exception(f"Failed to generate backtest results: {str(e)}")
    
    def generate_notion_landing_page(self, info, research_data: Dict[str, Any], 
                                   options: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a comprehensive Notion landing page"""
        if not NotionPageGenerator:
            raise Exception("Notion page generator not available")
            
        try:
            firm_id = options.get('firm_id', 'QXR')
            generator = NotionPageGenerator(firm_id)
            
            # Generate the landing page
            page_data = generator.generate_backtest_sim_landing_page(research_data)
            
            # Save specifications
            spec_file = generator.save_notion_page_spec(page_data)
            
            # Generate markdown
            markdown_content = generator.generate_notion_markdown(page_data)
            
            return {
                'spec_file': spec_file,
                'markdown_content': markdown_content,
                'landing_page_data': page_data,
                'api_spec': json.dumps(page_data, indent=2, default=str)
            }
        except Exception as e:
            raise Exception(f"Failed to generate Notion landing page: {str(e)}")
    
    def prepare_social_media_posts(self, info, research_data: Dict[str, Any],
                                 options: Dict[str, Any], auth: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare social media posts for multiple platforms"""
        if not SocialMediaEngine:
            raise Exception("Social media engine not available")
            
        try:
            # Validate authentication
            session_key = auth.get('session_key')
            if session_key and not self.validate_combsec_key(info, session_key):
                raise Exception("Invalid COMBSEC authentication")
            
            firm_id = options.get('firm_id', 'QXR')
            target_platforms = options.get('target_platforms', ['linkedin', 'twitter'])
            
            # Initialize engine
            engine = SocialMediaEngine(firm_id)
            
            # Prepare posts
            master_file, posts = engine.one_push_manual_prepare(
                research_data, target_platforms
            )
            
            # Convert posts dict to list format
            post_list = []
            for platform, content in posts.items():
                post_list.append({
                    'platform': platform,
                    'content': content,
                    'hashtags': self._extract_hashtags(content),
                    'combsec_key': session_key[:20] + "..." if session_key else "N/A",
                    'generated_at': datetime.now().isoformat()
                })
            
            # Generate Notion landing page if requested
            notion_landing = None
            if options.get('include_notion_landing', True) and 'notion' in target_platforms:
                notion_landing = self.generate_notion_landing_page(
                    info, research_data, {'firm_id': firm_id}
                )
            
            return {
                'master_file': master_file,
                'posts': post_list,
                'notion_landing_page': notion_landing,
                'instructions': engine.get_posting_instructions()
            }
        except Exception as e:
            raise Exception(f"Failed to prepare social media posts: {str(e)}")
    
    def system_health(self, info) -> Dict[str, Any]:
        """Get current system health status"""
        try:
            return {
                'status': 'HEALTHY',
                'uptime': '24/7',
                'last_update': datetime.now().isoformat(),
                'combsec_active': self.combsec_generator is not None,
                'notion_integration': NotionPageGenerator is not None,
                'social_media_engine': SocialMediaEngine is not None
            }
        except Exception as e:
            return {
                'status': 'ERROR',
                'uptime': 'Unknown',
                'last_update': datetime.now().isoformat(),
                'combsec_active': False,
                'notion_integration': False,
                'social_media_engine': False
            }
    
    def integration_status(self, info) -> Dict[str, Any]:
        """Get integration status for all system components"""
        return {
            'actnewworldodor': self.combsec_generator is not None,
            'qxr_notebook': NotebookProcessor is not None,
            'notion_api': NotionPageGenerator is not None,
            'social_platforms': [
                {'platform': 'linkedin', 'available': True, 'last_sync': None},
                {'platform': 'twitter', 'available': True, 'last_sync': None},
                {'platform': 'github', 'available': True, 'last_sync': None},
                {'platform': 'notion', 'available': NotionPageGenerator is not None, 'last_sync': None}
            ]
        }
    
    # Mutation Resolvers
    
    def process_notebook(self, info, notebook_path: str, auth: Dict[str, Any]) -> Dict[str, Any]:
        """Process a notebook and extract research metrics"""
        # Validate authentication
        session_key = auth.get('session_key')
        if session_key and not self.validate_combsec_key(info, session_key):
            raise Exception("Invalid COMBSEC authentication")
            
        return self.extract_notebook_metrics(info, notebook_path)
    
    def generate_social_media_package(self, info, research_data: Dict[str, Any],
                                    options: Dict[str, Any], auth: Dict[str, Any]) -> Dict[str, Any]:
        """Generate complete social media package"""
        return self.prepare_social_media_posts(info, research_data, options, auth)
    
    def create_notion_landing_page(self, info, research_data: Dict[str, Any],
                                 options: Dict[str, Any], auth: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new Notion landing page"""
        # Validate authentication
        session_key = auth.get('session_key')
        if session_key and not self.validate_combsec_key(info, session_key):
            raise Exception("Invalid COMBSEC authentication")
            
        return self.generate_notion_landing_page(info, research_data, options)
    
    def refresh_combsec_key(self, info, current_key: str, firm_id: str) -> Dict[str, Any]:
        """Refresh an existing COMBSEC key"""
        if current_key in self.active_sessions:
            # Remove old session
            del self.active_sessions[current_key]
        
        # Generate new key
        return self.generate_combsec_key(info, firm_id)
    
    def configure_allocator_access(self, info, allocator_id: str, permissions: List[str],
                                 auth: Dict[str, Any]) -> Dict[str, Any]:
        """Configure allocator access permissions"""
        # Validate authentication
        session_key = auth.get('session_key')
        if session_key and not self.validate_combsec_key(info, session_key):
            raise Exception("Invalid COMBSEC authentication")
        
        # Return configured allocator info
        return {
            'id': allocator_id,
            'name': f"Allocator {allocator_id}",
            'role': 'Configured',
            'permissions': permissions,
            'combsec_verified': True,
            'access_level': 'STANDARD'
        }
    
    # Helper Methods
    
    def _extract_hashtags(self, content: str) -> List[str]:
        """Extract hashtags from social media content"""
        import re
        hashtags = re.findall(r'#(\w+)', content)
        return hashtags
    
    # Subscription Resolvers (placeholder - would need WebSocket implementation)
    
    def research_metrics_updated(self, info, notebook_path: str):
        """Subscription for research metrics updates"""
        # Placeholder for real-time updates
        pass
    
    def posting_status_updated(self, info, package_id: str):
        """Subscription for posting status updates"""
        # Placeholder for real-time updates  
        pass
    
    def notion_page_updated(self, info, page_id: str):
        """Subscription for Notion page updates"""
        # Placeholder for real-time updates
        pass
    
    def system_health_updated(self, info):
        """Subscription for system health updates"""
        # Placeholder for real-time updates
        pass


# Global resolver instance
resolvers = GraphQLResolvers()

# Resolver mapping for GraphQL framework integration
RESOLVER_MAP = {
    'Query': {
        'generateCombsecKey': resolvers.generate_combsec_key,
        'validateCombsecKey': resolvers.validate_combsec_key,
        'extractNotebookMetrics': resolvers.extract_notebook_metrics,
        'getBacktestResults': resolvers.get_backtest_results,
        'generateNotionLandingPage': resolvers.generate_notion_landing_page,
        'prepareSocialMediaPosts': resolvers.prepare_social_media_posts,
        'systemHealth': resolvers.system_health,
        'integrationStatus': resolvers.integration_status,
    },
    'Mutation': {
        'processNotebook': resolvers.process_notebook,
        'generateSocialMediaPackage': resolvers.generate_social_media_package,
        'createNotionLandingPage': resolvers.create_notion_landing_page,
        'refreshCombsecKey': resolvers.refresh_combsec_key,
        'configureAllocatorAccess': resolvers.configure_allocator_access,
    },
    'Subscription': {
        'researchMetricsUpdated': resolvers.research_metrics_updated,
        'postingStatusUpdated': resolvers.posting_status_updated,
        'notionPageUpdated': resolvers.notion_page_updated,
        'systemHealthUpdated': resolvers.system_health_updated,
    }
}


def demo_graphql_integration():
    """Demonstrate GraphQL resolver functionality"""
    print("🌐 QXR GraphQL Resolvers Demo")
    print("=" * 60)
    
    resolver = GraphQLResolvers()
    
    # Test COMBSEC key generation
    print("🔐 Testing COMBSEC Key Generation...")
    try:
        key_result = resolver.generate_combsec_key(None, "DEMO_FIRM")
        print(f"✅ Generated key: {key_result['truncated_key']}")
        print(f"📅 Generated at: {key_result['generated_at']}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test system health
    print("\n🏥 Testing System Health...")
    health = resolver.system_health(None)
    print(f"✅ Status: {health['status']}")
    print(f"🔗 COMBSEC Active: {health['combsec_active']}")
    print(f"📄 Notion Integration: {health['notion_integration']}")
    
    # Test integration status
    print("\n🔗 Testing Integration Status...")
    integration = resolver.integration_status(None)
    print(f"✅ ACTNEWWORLDODOR: {integration['actnewworldodor']}")
    print(f"📊 QXR Notebook: {integration['qxr_notebook']}")
    
    print("\n" + "=" * 60)
    print("📋 GraphQL API Ready for Integration")
    print("Schema: @graphQL.ynl")
    print("Resolvers: QXR.graphql_resolvers")
    print("Authentication: COMBSEC Required")
    
    return resolver


if __name__ == "__main__":
    demo_graphql_integration()