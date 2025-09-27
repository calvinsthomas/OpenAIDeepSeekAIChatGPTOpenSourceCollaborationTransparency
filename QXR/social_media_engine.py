#!/usr/bin/env python3
"""
QXR Social Media Integration Engine
One-Push Manual Social Media Posting System

This module integrates with the ACTNEWWORLDODOR COMBSEC system to provide
secure, authenticated social media posting for quantitative research results.
Enhanced with Notion webpage publishing for Backtest Sim Landing Pages.
"""

import os
import sys
import json
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import requests
from urllib.parse import urlencode

# Import ACTNEWWORLDODOR COMBSEC system
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'ACTNEWWORLDODOR'))
from emoji_combsec_generator import EmojiCombsecGenerator

# Import Notion page generation functionality
from notion_page_generator import NotionPageGenerator


@dataclass
class SocialPlatform:
    """Configuration for a social media platform"""
    name: str
    api_endpoint: str
    auth_method: str
    max_length: int
    hashtag_support: bool
    media_support: bool


@dataclass
class PostContent:
    """Content structure for social media posts"""
    title: str
    content: str
    hashtags: List[str]
    media_urls: Optional[List[str]] = None
    research_data: Optional[Dict] = None
    combsec_key: Optional[str] = None


class SocialMediaEngine:
    """
    One-Push Manual Social Media Posting Engine
    
    Integrates QXR research outputs with multiple social platforms
    using ACTNEWWORLDODOR COMBSEC authentication
    """
    
    def __init__(self, firm_id: str = "QXR"):
        """Initialize the social media engine with COMBSEC authentication"""
        self.firm_id = firm_id
        self.combsec_generator = EmojiCombsecGenerator(firm_id)
        self.session_key = self.combsec_generator.generate_combsec_key()
        
        # Initialize Notion page generator for comprehensive webpage publishing
        self.notion_generator = NotionPageGenerator(firm_id)
        
        # Define supported platforms
        self.platforms = {
            'linkedin': SocialPlatform(
                name='LinkedIn',
                api_endpoint='https://api.linkedin.com/v2/shares',
                auth_method='oauth2',
                max_length=3000,
                hashtag_support=True,
                media_support=True
            ),
            'twitter': SocialPlatform(
                name='Twitter',
                api_endpoint='https://api.twitter.com/2/tweets',
                auth_method='oauth2',
                max_length=280,
                hashtag_support=True,
                media_support=True
            ),
            'github': SocialPlatform(
                name='GitHub',
                api_endpoint='https://api.github.com/repos/updates',
                auth_method='token',
                max_length=5000,
                hashtag_support=False,
                media_support=True
            ),
            'notion': SocialPlatform(
                name='Notion',
                api_endpoint='https://api.notion.com/v1/pages',
                auth_method='token',
                max_length=10000,
                hashtag_support=False,
                media_support=True
            )
        }
        
        self.post_history = []
        
    def authenticate_session(self) -> str:
        """Authenticate session using COMBSEC system"""
        os.environ['QXR_SOCIAL_COMBSEC_KEY'] = self.session_key
        return self.session_key
    
    def generate_research_post(self, research_data: Dict) -> PostContent:
        """
        Generate social media post content from research data
        
        Args:
            research_data: Dictionary containing research results
            
        Returns:
            PostContent object ready for posting
        """
        # Extract key metrics from research data
        signals = research_data.get('signals', 0)
        opportunities = research_data.get('opportunities', 0)
        signal_strength = research_data.get('signal_strength', 0)
        price_range = research_data.get('price_range', [0, 0])
        max_liquidity = research_data.get('max_liquidity', 0)
        
        # Create post content
        title = "🌐 QXR ETH Liquidity Research Update"
        
        content = f"""📊 Latest Statistical Arbitrage Analysis:
• Total signals: {signals}
• Recent opportunities: {opportunities}
• Avg signal strength: {signal_strength:.3f}

💡 ETH Price Range: ${price_range[0]:.0f} - ${price_range[1]:.0f}
📈 Max Liquidity: ${max_liquidity:.0f}

🔐 Verified with COMBSEC: {self.session_key[:20]}...
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""

        hashtags = [
            '#ETH', '#DeFi', '#QuantResearch', '#StatArb', 
            '#CryptoAnalysis', '#QXR', '#COMBSEC'
        ]
        
        return PostContent(
            title=title,
            content=content,
            hashtags=hashtags,
            research_data=research_data,
            combsec_key=self.session_key
        )
    
    def format_for_platform(self, post: PostContent, platform_name: str) -> str:
        """
        Format post content for specific platform requirements
        
        Args:
            post: PostContent object
            platform_name: Target platform name
            
        Returns:
            Formatted content string
        """
        platform = self.platforms.get(platform_name)
        if not platform:
            raise ValueError(f"Unsupported platform: {platform_name}")
        
        # Start with title and content
        formatted_content = f"{post.title}\n\n{post.content}"
        
        # Add hashtags if supported
        if platform.hashtag_support and post.hashtags:
            hashtag_string = ' '.join(post.hashtags)
            formatted_content = f"{formatted_content}\n\n{hashtag_string}"
        
        # Truncate if necessary
        if len(formatted_content) > platform.max_length:
            # Smart truncation preserving key information
            truncation_point = platform.max_length - 50
            formatted_content = formatted_content[:truncation_point] + "...\n\n🔗 Full report in comments"
        
        return formatted_content
    
    def prepare_manual_post(self, research_data: Dict, target_platforms: List[str]) -> Dict[str, str]:
        """
        Prepare manual posting content for multiple platforms
        
        Args:
            research_data: Research results to post
            target_platforms: List of platform names to target
            
        Returns:
            Dictionary mapping platform names to formatted content
        """
        # Generate base post content
        post = self.generate_research_post(research_data)
        
        # Format for each target platform
        formatted_posts = {}
        for platform_name in target_platforms:
            if platform_name in self.platforms:
                formatted_posts[platform_name] = self.format_for_platform(post, platform_name)
            else:
                print(f"⚠️ Warning: Unsupported platform '{platform_name}' skipped")
        
        return formatted_posts
    
    def save_posts_for_manual_publishing(self, posts: Dict[str, str], output_dir: str = "/tmp/qxr_social_posts") -> str:
        """
        Save formatted posts to files for manual publishing
        
        Args:
            posts: Dictionary of platform-formatted posts
            output_dir: Directory to save post files
            
        Returns:
            Path to the output directory
        """
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create a master file with all posts
        master_file = os.path.join(output_dir, f"qxr_social_posts_{timestamp}.md")
        
        with open(master_file, 'w', encoding='utf-8') as f:
            f.write(f"# QXR Social Media Posts - {timestamp}\n\n")
            f.write(f"🔐 COMBSEC Authentication: {self.session_key}\n\n")
            f.write("---\n\n")
            
            for platform, content in posts.items():
                f.write(f"## {self.platforms[platform].name}\n\n")
                f.write(f"**Max Length:** {self.platforms[platform].max_length} characters\n")
                f.write(f"**Content Length:** {len(content)} characters\n\n")
                f.write("```\n")
                f.write(content)
                f.write("\n```\n\n")
                f.write("---\n\n")
                
                # Save individual platform files
                platform_file = os.path.join(output_dir, f"{platform}_{timestamp}.txt")
                with open(platform_file, 'w', encoding='utf-8') as pf:
                    pf.write(content)
        
        return master_file
    
    def one_push_manual_prepare(self, research_data: Dict, 
                               target_platforms: Optional[List[str]] = None) -> Tuple[str, Dict[str, str]]:
        """
        One-push preparation for manual social media posting with Backtest Sim Landing Page
        
        Args:
            research_data: Research results to post
            target_platforms: List of platforms (defaults to all available)
            
        Returns:
            Tuple of (master_file_path, platform_posts_dict)
        """
        if target_platforms is None:
            target_platforms = list(self.platforms.keys())
        
        print(f"🌐 QXR Social Media Engine - One-Push Manual Prepare")
        print(f"🔐 COMBSEC Session: {self.session_key[:30]}...")
        print(f"🎯 Target Platforms: {', '.join(target_platforms)}")
        
        # Prepare posts for all platforms
        formatted_posts = self.prepare_manual_post(research_data, target_platforms)
        
        # Generate Backtest Sim Landing Page for Notion if Notion is in target platforms
        notion_landing_page = None
        if 'notion' in target_platforms:
            print("📄 Generating Backtest Sim Main Landing Page for Notion...")
            landing_page_data = self.notion_generator.generate_backtest_sim_landing_page(research_data)
            
            # Save comprehensive Notion page specification
            spec_file = self.notion_generator.save_notion_page_spec(landing_page_data)
            
            # Generate Notion-compatible markdown
            notion_markdown = self.notion_generator.generate_notion_markdown(landing_page_data)
            
            # Replace simple Notion post with comprehensive landing page
            formatted_posts['notion'] = notion_markdown
            
            notion_landing_page = {
                'spec_file': spec_file,
                'landing_page_data': landing_page_data,
                'markdown_content': notion_markdown
            }
            
            print("✅ Backtest Sim Landing Page generated successfully")
            print(f"📊 Performance: {landing_page_data['backtest_results'].total_return:.2f}% return")
            print(f"👥 Allocators: {len(landing_page_data['allocator_access'])} configured")
        
        # Save to files for manual publishing
        master_file = self.save_posts_for_manual_publishing(formatted_posts)
        
        print(f"✅ Posts prepared and saved to: {master_file}")
        print(f"📝 Generated {len(formatted_posts)} platform-specific posts")
        
        # Store in history with landing page data
        history_entry = {
            'timestamp': datetime.now().isoformat(),
            'platforms': target_platforms,
            'master_file': master_file,
            'combsec_key': self.session_key,
            'research_data': research_data
        }
        
        if notion_landing_page:
            history_entry['notion_landing_page'] = {
                'spec_file': notion_landing_page['spec_file'],
                'has_backtest_sim': True,
                'allocator_count': len(notion_landing_page['landing_page_data']['allocator_access'])
            }
        
        self.post_history.append(history_entry)
        
        return master_file, formatted_posts
    
    def get_posting_instructions(self) -> str:
        """Generate instructions for manual posting"""
        instructions = """
🌐 QXR SOCIAL MEDIA POSTING INSTRUCTIONS

1. AUTHENTICATION:
   - Use COMBSEC key for verification
   - Include key reference in posts for transparency

2. PLATFORM-SPECIFIC POSTING:
   - LinkedIn: Professional tone, full content
   - Twitter: Concise version, thread if needed  
   - GitHub: Technical focus, link to repo
   - Notion: **BACKTEST SIM LANDING PAGE** - Comprehensive trading system documentation

3. NOTION BACKTEST SIM LANDING PAGE:
   - **VERY IMPORTANT**: Creates comprehensive quantitative trading system webpage
   - Includes peer-reviewed validation (Journal of Financial Economics)
   - Multi-allocator shared access with NEWWORLDODOR security context
   - AI-driven workflow automation indicators
   - Statistical arbitrage performance metrics and risk analysis
   - Import markdown directly or use JSON API specification

4. MANUAL POSTING PROCESS:
   a) Copy content from generated files
   b) Login to each platform manually
   c) Paste formatted content
   d) **For Notion**: Import landing page markdown or use API spec
   e) Configure allocator permissions as specified
   f) Schedule or publish immediately
   g) Verify posts are live

5. VERIFICATION:
   - Check all links work
   - Verify hashtags display correctly
   - Confirm COMBSEC reference is included
   - **Notion**: Verify allocator access controls
   - Monitor engagement metrics

6. SECURITY:
   - Never share raw COMBSEC keys
   - Use truncated keys in public posts
   - Keep full session logs private
   - **NEWWORLDODOR context**: Follow security protocols for shared spaces
        """
        return instructions


def demo_usage():
    """Demonstrate the social media engine usage"""
    print("🌐 QXR Social Media Engine Demo")
    print("=" * 50)
    
    # Initialize engine
    engine = SocialMediaEngine("QXR")
    
    # Sample research data (would come from notebook analysis)
    sample_research_data = {
        'signals': 45,
        'opportunities': 8,
        'signal_strength': 1.247,
        'price_range': [3420, 3580],
        'max_liquidity': 12500000,
        'strategy': 'ETH Statistical Arbitrage',
        'timeframe': '24h'
    }
    
    # Prepare posts for manual publishing
    master_file, posts = engine.one_push_manual_prepare(
        sample_research_data,
        target_platforms=['linkedin', 'twitter', 'github']
    )
    
    print(f"\n📁 Posts saved to: {master_file}")
    
    # Show instructions
    print("\n" + "=" * 50)
    print(engine.get_posting_instructions())
    
    return engine


if __name__ == "__main__":
    # Run demo
    demo_usage()