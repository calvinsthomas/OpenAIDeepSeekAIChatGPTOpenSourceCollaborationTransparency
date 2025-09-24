#!/usr/bin/env python3
"""
QXR Social Media Integration Engine
One-Push Manual Social Media Posting System

This module integrates with the ACTNEWWORLDODOR COMBSEC system to provide
secure, authenticated social media posting for quantitative research results.
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
sys.path.append('../ACTNEWWORLDODOR')
from emoji_combsec_generator import EmojiCombsecGenerator


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
    
    def _sanitize_numeric_value(self, value, default=0):
        """
        Sanitize numeric values to handle edge cases like inf, nan, and invalid types
        
        Args:
            value: Input value to sanitize
            default: Default value to use if sanitization fails
            
        Returns:
            Sanitized numeric value
        """
        try:
            # Handle None
            if value is None:
                return default
                
            # Convert to float first
            if isinstance(value, str):
                # Try to convert string to number
                try:
                    value = float(value)
                except (ValueError, TypeError):
                    return default
            
            # Handle inf and nan
            if isinstance(value, (int, float)):
                if value == float('inf') or value == float('-inf'):
                    return 999999999 if value == float('inf') else -999999999
                if value != value:  # Check for NaN
                    return default
                # Clamp extremely large values
                if abs(value) > 1e15:
                    return 1e15 if value > 0 else -1e15
                return value
            
            return default
        except:
            return default
    
    def generate_research_post(self, research_data: Dict) -> PostContent:
        """
        Generate social media post content from research data
        
        Args:
            research_data: Dictionary containing research results
            
        Returns:
            PostContent object ready for posting
        """
        # Safely extract and sanitize key metrics from research data
        signals = self._sanitize_numeric_value(research_data.get('signals', 0), 0)
        opportunities = self._sanitize_numeric_value(research_data.get('opportunities', 0), 0)
        signal_strength = self._sanitize_numeric_value(research_data.get('signal_strength', 0), 0.0)
        max_liquidity = self._sanitize_numeric_value(research_data.get('max_liquidity', 0), 0)
        
        # Handle price range safely
        price_range = research_data.get('price_range', [0, 0])
        if not isinstance(price_range, (list, tuple)) or len(price_range) < 2:
            price_range = [0, 0]
        
        price_low = self._sanitize_numeric_value(price_range[0], 0)
        price_high = self._sanitize_numeric_value(price_range[1], 0)
        
        # Extract custom strategy or notes with unicode support
        strategy = research_data.get('strategy', '')
        notes = research_data.get('notes', '')
        custom_content = ""
        
        # Include custom strategy if present
        if strategy and strategy != 'Statistical Arbitrage':
            custom_content += f"\n• Strategy: {strategy}"
        
        # Include notes if present  
        if notes:
            custom_content += f"\n• Notes: {notes}"
        
        # Ensure session key is available
        session_key_display = self.session_key[:20] if self.session_key else "UNAVAILABLE"
        
        # Create post content with safe formatting
        title = "🌐 QXR ETH Liquidity Research Update"
        
        try:
            content = f"""📊 Latest Statistical Arbitrage Analysis:
• Total signals: {int(signals)}
• Recent opportunities: {int(opportunities)}
• Avg signal strength: {signal_strength:.3f}{custom_content}

💡 ETH Price Range: ${price_low:.0f} - ${price_high:.0f}
📈 Max Liquidity: ${max_liquidity:.0f}

🔐 Verified with COMBSEC: {session_key_display}...
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""
        except Exception as e:
            # Fallback content if formatting fails
            content = f"""📊 Latest Statistical Arbitrage Analysis:
• Total signals: {signals}
• Recent opportunities: {opportunities}
• Signal data processing completed{custom_content}

🔐 Verified with COMBSEC: {session_key_display}...
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
            combsec_key=self.session_key or "FALLBACK_KEY"
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
        
        # Handle edge cases with empty or None content
        title = post.title if post.title else "🌐 QXR Research Update"
        content = post.content if post.content else "Research data processing completed."
        
        # Start with title and content
        formatted_content = f"{title}\n\n{content}"
        
        # Add hashtags if supported
        if platform.hashtag_support and post.hashtags:
            hashtag_string = ' '.join(post.hashtags)
            formatted_content = f"{formatted_content}\n\n{hashtag_string}"
        
        # Always include COMBSEC reference if available
        if post.combsec_key and post.combsec_key != "FALLBACK_KEY":
            if "COMBSEC:" not in formatted_content:
                formatted_content += f"\n\n🔐 Verified with COMBSEC: {post.combsec_key[:20]}..."
        
        # Ensure we have some content even if everything was empty
        if not formatted_content.strip():
            formatted_content = f"🌐 QXR Research Update\n\nData processing completed.\n\n🔐 Session verified"
        
        # Truncate if necessary but preserve key information
        if len(formatted_content) > platform.max_length:
            # Smart truncation preserving COMBSEC reference
            combsec_line = "🔐 Verified with COMBSEC:"
            combsec_idx = formatted_content.find(combsec_line)
            
            if combsec_idx >= 0:
                # Extract COMBSEC line and what follows
                combsec_part = formatted_content[combsec_idx:]
                before_combsec = formatted_content[:combsec_idx].rstrip()
                
                # Calculate space needed for COMBSEC part (limit to reasonable length)
                combsec_part_lines = combsec_part.split('\n')
                essential_combsec = combsec_part_lines[0]  # Just the COMBSEC line
                if len(combsec_part_lines) > 1:
                    essential_combsec += '\n' + combsec_part_lines[1]  # And timestamp if present
                
                # Calculate available space for main content
                footer = "\n\n🔗 More details..."
                space_for_content = platform.max_length - len(essential_combsec) - len(footer)
                
                if len(before_combsec) > space_for_content:
                    # Truncate main content but preserve structure
                    truncated_content = before_combsec[:space_for_content - 3] + "..."
                    formatted_content = truncated_content + '\n\n' + essential_combsec
                else:
                    # Content fits with COMBSEC, just use essential parts
                    formatted_content = before_combsec + '\n\n' + essential_combsec
            else:
                # No COMBSEC found, standard truncation
                formatted_content = formatted_content[:platform.max_length - 20] + "...\n\n🔗 More"
            
            # Final length check
            if len(formatted_content) > platform.max_length:
                formatted_content = formatted_content[:platform.max_length - 3] + "..."
        
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
        One-push preparation for manual social media posting
        
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
        
        # Save to files for manual publishing
        master_file = self.save_posts_for_manual_publishing(formatted_posts)
        
        print(f"✅ Posts prepared and saved to: {master_file}")
        print(f"📝 Generated {len(formatted_posts)} platform-specific posts")
        
        # Store in history
        self.post_history.append({
            'timestamp': datetime.now().isoformat(),
            'platforms': target_platforms,
            'master_file': master_file,
            'combsec_key': self.session_key,
            'research_data': research_data
        })
        
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
   - Notion: Detailed analysis, embedded charts

3. MANUAL POSTING PROCESS:
   a) Copy content from generated files
   b) Login to each platform manually
   c) Paste formatted content
   d) Add any platform-specific formatting
   e) Schedule or publish immediately
   f) Verify posts are live

4. VERIFICATION:
   - Check all links work
   - Verify hashtags display correctly
   - Confirm COMBSEC reference is included
   - Monitor engagement metrics

5. SECURITY:
   - Never share raw COMBSEC keys
   - Use truncated keys in public posts
   - Keep full session logs private
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