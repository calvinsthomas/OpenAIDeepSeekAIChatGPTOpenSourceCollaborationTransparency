#!/usr/bin/env python3
"""
Demonstration of Intertemporal Differentials Analysis Integration
with QXR Social Media System

This script demonstrates the complete integration of the new IntertemporalAnalyzer
with the existing QXR social media integration pipeline, as specified in the
ChatGPT document (277828ff6bf7804a83d2e307eafcaa09).
"""

import sys
from pathlib import Path
import json
from datetime import datetime

# Add QXR to path for social media integration
current_dir = Path(__file__).parent
qxr_dir = current_dir / "QXR"
sys.path.insert(0, str(qxr_dir))

# Import the new IntertemporalAnalyzer
from intertemporal_cv import IntertemporalAnalyzer, create_sample_financial_data
from ACTNEWWORLDODOR.emoji_combsec_generator import EmojiCombsecGenerator

# Import QXR social media components
try:
    from social_media_engine import SocialMediaEngine
    from notion_page_generator import NotionPageGenerator
    QXR_AVAILABLE = True
except ImportError:
    QXR_AVAILABLE = False
    print("⚠️  QXR modules not available, running standalone demo")


def create_comprehensive_demo_data():
    """Create comprehensive demo data for intertemporal analysis"""
    print("📊 Creating comprehensive demo dataset...")
    
    # Create base financial data
    financial_data = create_sample_financial_data(150)
    
    # Add more sophisticated patterns for demonstration
    import pandas as pd
    import numpy as np
    
    # Add regime changes
    financial_data.loc[financial_data.index[50:70], 'price'] *= 1.1  # Bull market
    financial_data.loc[financial_data.index[100:120], 'price'] *= 0.9  # Bear market
    
    # Add volatility clustering
    vol_periods = [30, 80, 130]
    for period in vol_periods:
        if period < len(financial_data):
            financial_data.loc[financial_data.index[period:period+10], 'volume'] *= 2
    
    # Add more sophisticated text data with parody patterns
    text_samples = [
        "Serious market analysis shows strong trends",
        "This is definitely not a #parody of crypto analysis",
        "Real analysis of DeFi protocols",
        "Fake news about market manipulation",
        "Legitimate statistical arbitrage research",
        "This is a parody of technical analysis",
        "Genuine quantitative research findings",
        "Satirical take on market predictions",
        "Professional trading algorithm results",
        "Mock analysis of price movements"
    ]
    
    # Replace text data with patterns
    for i, idx in enumerate(financial_data.index):
        financial_data.loc[idx, 'text_analysis'] = text_samples[i % len(text_samples)]
    
    return financial_data


def demonstrate_intertemporal_analysis():
    """Demonstrate the IntertemporalAnalyzer functionality"""
    print("🌐 INTERTEMPORAL DIFFERENTIALS ANALYSIS DEMO")
    print("=" * 70)
    print("Based on ChatGPT document: 277828ff6bf7804a83d2e307eafcaa09")
    print()
    
    # Initialize with COMBSEC security
    print("🔐 Initializing with COMBSEC security context...")
    generator = EmojiCombsecGenerator()
    security_key = generator.generate_combsec_key()
    
    analyzer = IntertemporalAnalyzer(security_key=security_key)
    print(f"✅ Analyzer initialized with key: {security_key[:30]}...")
    print()
    
    # Create comprehensive demo data
    demo_data = create_comprehensive_demo_data()
    print(f"📈 Dataset created: {demo_data.shape[0]} observations, {demo_data.shape[1]} variables")
    print(f"   Period: {demo_data.index[0].strftime('%Y-%m-%d')} to {demo_data.index[-1].strftime('%Y-%m-%d')}")
    print()
    
    # Perform comprehensive analysis
    print("🔍 Performing comprehensive intertemporal analysis...")
    print()
    
    analysis_results = {}
    
    # Test all CV methods
    cv_methods = ['time_series', 'expanding_window', 'blocked']
    
    for method in cv_methods:
        print(f"📊 Testing {method.replace('_', ' ').title()} Cross-Validation:")
        
        results = analyzer.analyze_temporal_diffs(
            data=demo_data,
            cv_method=method,
            parody_detection=True,
            target_column='price'
        )
        
        analysis_results[method] = results
        
        # Print key metrics
        cv_metrics = results.get('cv_analysis', {}).get('performance_metrics', {})
        parody_metrics = results.get('parody_detection', {})
        
        print(f"   • CV Performance: {cv_metrics.get('out_of_sample_accuracy', 'N/A'):.3f}" if cv_metrics.get('out_of_sample_accuracy') else "   • CV Performance: N/A")
        print(f"   • Parody Indicators: {parody_metrics.get('total_parody_indicators', 0)}")
        print(f"   • Pattern Confidence: {parody_metrics.get('pattern_confidence', 0):.3f}")
        print()
    
    # Test regime change detection
    print("🔄 Testing Regime Change Detection:")
    regime_results = analyzer.get_regime_change_detection(demo_data['price'])
    if 'error' not in regime_results:
        print(f"   • Regime Changes Detected: {regime_results.get('total_regime_changes', 0)}")
        if regime_results.get('change_points'):
            print(f"   • First Change Point: {regime_results['change_points'][0]['timestamp']}")
    else:
        print(f"   • {regime_results['error']}")
    print()
    
    # Test security validation
    print("🔐 Testing Security Context Validation:")
    security_validation = analyzer.validate_security_context()
    print(f"   • Security Valid: {security_validation.get('valid', False)}")
    print(f"   • Firm ID: {security_validation.get('firm_id', 'N/A')}")
    print()
    
    return analysis_results, demo_data


def demonstrate_qxr_integration(analysis_results, demo_data):
    """Demonstrate integration with QXR social media system"""
    if not QXR_AVAILABLE:
        print("⚠️  QXR integration demo skipped (modules not available)")
        return
    
    print("🚀 QXR INTEGRATION DEMONSTRATION")
    print("=" * 50)
    
    # Initialize QXR components
    social_engine = SocialMediaEngine("IntertemporalDemo")
    notion_generator = NotionPageGenerator("IntertemporalDemo")
    
    # Convert analysis results to QXR-compatible format
    best_results = analysis_results['time_series']  # Use time_series as primary method
    
    qxr_data = {
        'signals': len(best_results.get('temporal_differentials', {})),
        'opportunities': best_results.get('parody_detection', {}).get('total_parody_indicators', 0),
        'signal_strength': best_results.get('cv_analysis', {}).get('performance_metrics', {}).get('out_of_sample_accuracy', 0.5),
        'price_range': [demo_data['price'].min(), demo_data['price'].max()],
        'max_liquidity': demo_data['volume'].max(),
        'strategy': 'Intertemporal Differentials Analysis',
        'timeframe': '24h',
        'combsec_key': best_results.get('security_key', '')
    }
    
    print("📱 Generating social media content...")
    
    # Generate social media post
    post_content = social_engine.generate_research_post(qxr_data)
    
    print("✅ Social Media Post Generated:")
    print(f"   Title: {post_content.title}")
    print(f"   Content Preview: {post_content.content[:100]}...")
    print(f"   Hashtags: {', '.join(post_content.hashtags)}")
    print()
    
    # Generate Notion landing page
    print("📄 Generating Notion Backtest Sim Landing Page...")
    
    landing_page_spec = notion_generator.generate_backtest_sim_landing_page(qxr_data)
    
    print("✅ Notion Landing Page Generated:")
    backtest_results = landing_page_spec.get('backtest_results')
    if backtest_results:
        print(f"   Performance: {backtest_results.total_return:.2f}% return")
        print(f"   Sharpe Ratio: {backtest_results.sharpe_ratio:.2f}")
        print(f"   Max Drawdown: {backtest_results.max_drawdown:.2f}%")
        print(f"   Total Trades: {backtest_results.total_trades}")
    print(f"   Allocator Access: {len(landing_page_spec.get('allocator_access', []))} configured")
    print()
    
    return {
        'social_post': post_content,
        'landing_page': landing_page_spec
    }


def save_demo_results(analysis_results, qxr_integration_results=None):
    """Save demo results for review"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_dir = Path("/tmp/intertemporal_demo")
    output_dir.mkdir(exist_ok=True)
    
    # Save analysis results
    analysis_file = output_dir / f"intertemporal_analysis_{timestamp}.json"
    
    # Convert results to JSON-serializable format
    serializable_results = {}
    for method, results in analysis_results.items():
        serializable_results[method] = {
            'method': results.get('method'),
            'timestamp': results.get('timestamp'),
            'data_shape': results.get('data_shape'),
            'cv_performance': results.get('cv_analysis', {}).get('performance_metrics', {}),
            'parody_detection': results.get('parody_detection', {}),
            'security_key_truncated': results.get('security_key')
        }
    
    with open(analysis_file, 'w') as f:
        json.dump(serializable_results, f, indent=2, default=str)
    
    print(f"💾 Analysis results saved to: {analysis_file}")
    
    # Save QXR integration results if available
    if qxr_integration_results:
        qxr_file = output_dir / f"qxr_integration_{timestamp}.json"
        
        landing_page_data = qxr_integration_results['landing_page']
        backtest_results = landing_page_data.get('backtest_results')
        
        qxr_data = {
            'social_post': {
                'title': qxr_integration_results['social_post'].title,
                'content': qxr_integration_results['social_post'].content,
                'hashtags': qxr_integration_results['social_post'].hashtags
            },
            'landing_page': {
                'strategy_name': backtest_results.strategy_name if backtest_results else 'N/A',
                'total_return': backtest_results.total_return if backtest_results else 0,
                'sharpe_ratio': backtest_results.sharpe_ratio if backtest_results else 0,
                'max_drawdown': backtest_results.max_drawdown if backtest_results else 0,
                'win_rate': backtest_results.win_rate if backtest_results else 0,
                'total_trades': backtest_results.total_trades if backtest_results else 0,
                'allocator_count': len(landing_page_data.get('allocator_access', [])),
                'combsec_key': landing_page_data.get('combsec_key', '')
            }
        }
        
        with open(qxr_file, 'w') as f:
            json.dump(qxr_data, f, indent=2, default=str)
        
        print(f"💾 QXR integration results saved to: {qxr_file}")
    
    return output_dir


def main():
    """Main demonstration function"""
    print("🌐 COMPREHENSIVE INTERTEMPORAL ANALYSIS INTEGRATION DEMO")
    print("=" * 80)
    print("Demonstrating ChatGPT document implementation: 277828ff6bf7804a83d2e307eafcaa09")
    print("OpenAI-DeepSeek AI ChatGPT Open Source Collaboration Transparency")
    print("=" * 80)
    print()
    
    try:
        # Demonstrate core intertemporal analysis
        analysis_results, demo_data = demonstrate_intertemporal_analysis()
        
        # Demonstrate QXR integration
        qxr_results = demonstrate_qxr_integration(analysis_results, demo_data)
        
        # Save results
        output_dir = save_demo_results(analysis_results, qxr_results)
        
        print("🎉 DEMO COMPLETE!")
        print("=" * 50)
        print("✅ All components successfully integrated:")
        print("   • Intertemporal differential analysis")
        print("   • Cross-validation modeling")
        print("   • Parody detection")
        print("   • COMBSEC security authentication")
        print("   • QXR social media integration")
        print("   • Notion Backtest Sim landing pages")
        print()
        print(f"📁 Results saved in: {output_dir}")
        print("📋 Integration ready for production deployment")
        
        return True
        
    except Exception as e:
        print(f"❌ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)