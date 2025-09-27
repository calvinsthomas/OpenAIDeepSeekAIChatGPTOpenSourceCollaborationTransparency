#!/usr/bin/env python3
"""
QXR Main Social Media Integration Script
One-Push Manual Social Media Posting for ETHLIQENGDOTIPYNBNTBK Research

This is the main entry point for the QXR social media integration system.
It processes the ETHLIQENGDOTIPYNBNTBK notebook and generates formatted
social media posts for manual publishing across multiple platforms.
"""

import sys
import os
import time
from datetime import datetime
from pathlib import Path

# Add current directory to path for imports
current_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(current_dir))

from social_media_engine import SocialMediaEngine
from notebook_to_social import NotebookProcessor

# Import enhanced bridge integration
try:
    from qxr_bridge_integration import EnhancedSocialMediaEngine
    BRIDGE_AVAILABLE = True
    print("🚀 QXR Bridge integration loaded successfully")
except ImportError:
    BRIDGE_AVAILABLE = False
    print("⚠️  Bridge integration not available, using standard engine")


def main():
    """Main function for QXR social media integration"""
    print("🌐 QXR ETHLIQENGDOTIPYNBNTBK Social Media Integration")
    print("=" * 70)
    print("One-Push Manual Social Media Posting Engine")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Initialize components
    notebook_path = current_dir / "ETHLIQENGDOTIPYNBNTBK.ipynb"
    
    if not notebook_path.exists():
        print(f"❌ Error: Notebook not found at {notebook_path}")
        print("Please ensure the ETHLIQENGDOTIPYNBNTBK.ipynb file exists in the QXR directory.")
        return False
    
    print(f"📓 Processing notebook: {notebook_path}")
    
    # Initialize processor and engine with bridge if available
    processor = NotebookProcessor(str(notebook_path))
    
    if BRIDGE_AVAILABLE:
        print("🚀 Using Enhanced Social Media Engine with Rust-C-Python Bridge")
        engine = EnhancedSocialMediaEngine("QXR")
    else:
        print("📱 Using Standard Social Media Engine")
        engine = SocialMediaEngine("QXR")
    
    # Extract research metrics from notebook
    print("🔍 Extracting research metrics...")
    research_data = processor.extract_research_metrics()
    
    if not research_data:
        print("❌ Failed to extract research data from notebook")
        return False
    
    print("✅ Research metrics extracted successfully:")
    for key, value in research_data.items():
        if key not in ['timestamp']:
            print(f"   • {key.replace('_', ' ').title()}: {value}")
    
    print()
    
    # Process with enhanced engine if available
    if BRIDGE_AVAILABLE and hasattr(engine, 'process_research_metrics'):
        print("🚀 Processing with Enhanced Engine (Bridge)...")
        start_time = time.time()
        
        results = engine.process_research_metrics(research_data)
        processing_time = time.time() - start_time
        
        print(f"✅ Performance Score: {results['performance_score']:.2f}")
        print(f"⏱️  Processing Time: {results['processing_time_ms']:.2f}ms")
        print(f"🔧 Bridge Version: {results['bridge_info']['version']}")
        
        print()
        print("📱 Preparing social media posts with bridge acceleration...")
        
        # Use enhanced one-push preparation
        target_platforms = ['linkedin', 'twitter', 'github', 'notion']
        master_file, posts = engine.one_push_manual_prepare(research_data, target_platforms)
        
    else:
        print("🔐 Initializing COMBSEC authentication...")
        session_key = engine.authenticate_session()
        print(f"✅ Authenticated with key: {session_key[:30]}...")
        
        # Prepare social media posts
        print()
        print("📱 Preparing social media posts...")
        
        target_platforms = ['linkedin', 'twitter', 'github', 'notion']
        master_file, posts = engine.one_push_manual_prepare(research_data, target_platforms)
    
    print()
    print("✅ Social media posts prepared successfully!")
    print(f"📁 Master file: {master_file}")
    print(f"📝 Generated posts for {len(posts)} platforms: {', '.join(posts.keys())}")
    
    # Display sample content
    print()
    print("=" * 70)
    print("📄 SAMPLE POST CONTENT (LinkedIn):")
    print("-" * 40)
    if 'linkedin' in posts:
        sample_content = posts['linkedin']
        if len(sample_content) > 400:
            sample_content = sample_content[:400] + "\\n... [content truncated]"
        print(sample_content)
    print("-" * 40)
    
    # Display posting instructions
    print()
    print("=" * 70)
    print("📋 MANUAL POSTING INSTRUCTIONS:")
    print(engine.get_posting_instructions())
    
    print("=" * 70)
    print("🎯 NEXT STEPS:")
    print("1. Open the master file for all platform-specific content")
    print("2. Copy content for each platform from individual files")
    print("3. Login to each social media platform manually")
    print("4. Paste and customize content as needed")
    print("5. Publish posts and monitor engagement")
    print()
    print(f"🔗 All files are saved in: {Path(master_file).parent}")
    print()
    print("🎉 QXR Social Media Integration Complete!")
    
    return True


def show_help():
    """Show help information"""
    print("QXR Social Media Integration - Help")
    print("=" * 50)
    print()
    print("This script processes the ETHLIQENGDOTIPYNBNTBK.ipynb notebook")
    print("and generates formatted social media posts for manual publishing.")
    print()
    print("Usage:")
    print("  python3 qxr_main.py           - Run the integration")
    print("  python3 qxr_main.py --help    - Show this help")
    print("  python3 qxr_main.py --test    - Run tests")
    print("  python3 qxr_main.py --graphql  - GraphQL API demo")
    print("  python3 qxr_main.py --custom   - Run custom workflow loader")
    print()
    print("Files generated:")
    print("  • Master markdown file with all platform posts")
    print("  • Individual text files for each platform")
    print("  • COMBSEC authentication logs")
    print()
    print("Supported platforms:")
    print("  • LinkedIn (professional focus)")
    print("  • Twitter (concise format)")
    print("  • GitHub (technical focus)")
    print("  • Notion (detailed analysis)")
    print()
    print("Security:")
    print("  • COMBSEC key authentication")
    print("  • Secure key truncation in public posts")
    print("  • Integration with ACTNEWWORLDODOR system")


def run_tests():
    """Run the test suite"""
    print("🧪 Running QXR Social Media Integration Tests...")
    print()
    
    try:
        from test_social_integration import run_comprehensive_tests
        social_tests_passed = run_comprehensive_tests()
        
        # Also run custom workflow loader tests
        try:
            from test_custom_workflow_loader import run_custom_workflow_tests
            custom_tests_passed = run_custom_workflow_tests()
            return social_tests_passed and custom_tests_passed
        except ImportError:
            print("⚠️ Custom workflow loader tests not available")
            return social_tests_passed
            
    except ImportError as e:
        print(f"❌ Error importing test module: {e}")
        return False


def run_graphql_demo():
    """Run GraphQL API demonstration"""
    print("🌐 Running QXR GraphQL API Demo...")
    print()
    
    try:
        from graphql_resolvers import demo_graphql_integration
        demo_graphql_integration()
        return True
    except ImportError as e:
        print(f"❌ Error importing GraphQL resolvers: {e}")
        return False


def run_custom_workflow():
    """Run custom workflow loader"""
    print("🎬 Running Custom Workflow Loader...")
    print()
    
    try:
        from custom_workflow_loader import CustomWorkflowLoader
        loader = CustomWorkflowLoader()
        
        if loader.check_command_file():
            return loader.execute_custom_workflow()
        else:
            print("❌ No custom workflow command file found")
            print(f"Expected location: {loader.command_file}")
            return False
    except ImportError as e:
        print(f"❌ Error importing custom workflow loader: {e}")
        return False


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--help" or sys.argv[1] == "-h":
            show_help()
            sys.exit(0)
        elif sys.argv[1] == "--test":
            success = run_tests()
            sys.exit(0 if success else 1)
        elif sys.argv[1] == "--graphql":
            success = run_graphql_demo()
            sys.exit(0 if success else 1)
        elif sys.argv[1] == "--custom":
            success = run_custom_workflow()
            sys.exit(0 if success else 1)
        else:
            print(f"Unknown argument: {sys.argv[1]}")
            print("Use --help for usage information")
            sys.exit(1)
    
    # Run main integration
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\\n🛑 Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)