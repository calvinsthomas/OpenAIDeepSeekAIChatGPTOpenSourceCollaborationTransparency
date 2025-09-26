# QXR - Quant Use Case Research Social Media Integration with Backtest Sim Landing Pages

## Overview

The QXR (Quant Use Case Research) social media integration system provides a **one-push manual** solution for posting research results from the `ETHLIQENGDOTIPYNBNTBK.ipynb` notebook to multiple social media platforms. Enhanced with **Agentic AI-driven Backtest Sim Main Landing Page** generation for comprehensive quantitative trading system documentation within Notion. This system integrates with the existing ACTNEWWORLDODOR COMBSEC authentication system for secure, verified posting.

## Problem Solved

The system addresses Calvin Thomas's use of Agentic AI within Notion to publish webpages for quantitative trading systems, specifically creating **"Backtest Sim Main Landing Pages"** for crypto statistical arbitrage strategies. The solution provides peer-reviewed validation (Journal of Financial Economics), multi-allocator shared access with NEWWORLDODOR security context, and AI-driven workflow automation.

### Key Features

- 🌐 **One-Push Manual Posting**: Single command generates posts for all platforms
- 🔐 **COMBSEC Integration**: Uses existing U+1F310 (🌐) emoji-based security keys  
- 📊 **Research Data Extraction**: Automatically parses Jupyter notebook outputs
- 📱 **Multi-Platform Support**: LinkedIn, Twitter, GitHub, **Notion with Landing Pages**
- 🎯 **Platform-Specific Formatting**: Optimized content for each social platform
- 📁 **Manual Publishing Workflow**: Generates files for copy-paste posting
- 🚨 **VERY IMPORTANT**: Comprehensive Backtest Sim Landing Pages for Notion
- 👥 **Multi-Allocator Access**: Shared workspace with controlled permissions
- 🤖 **AI-Driven Workflows**: Agentic AI integration with automation indicators
- 📚 **Peer-Reviewed Validation**: Journal of Financial Economics compliance
- 🔒 **NEWWORLDODOR Security**: Enhanced security context for shared spaces

## Enhanced Notion Integration

### Backtest Sim Main Landing Page
When Notion is included in target platforms, the system automatically generates comprehensive landing pages instead of simple posts:

- **Performance Summary Tables**: Statistical arbitrage metrics with peer-review benchmarks
- **Risk Analysis**: Max drawdown, Sharpe ratios, win rates
- **Multi-Allocator Access Control**: Configured permissions for team collaboration
- **AI Workflow Indicators**: Automation status and productivity metrics
- **NEWWORLDODOR Security Context**: High-priority access controls
- **Peer-Review References**: Journal of Financial Economics validation

### Key Landing Page Sections
1. **🚨 VERY IMPORTANT**: Priority callout for urgent strategies
2. **📊 Statistical Arbitrage Performance Summary**: Comprehensive metrics table
3. **🔬 Peer-Reviewed Validation**: Academic study references
4. **🔐 NEWWORLDODOR Security Context**: COMBSEC authentication details
5. **🤖 AI-Driven Workflow Automation**: McKinsey productivity study references
6. **👥 Multi-Allocator Shared Access**: Team member permissions table
7. **⚠️ Security Considerations**: Shared digital space risk mitigation

## File Structure

```
QXR/
├── ETHLIQENGDOTIPYNBNTBK.ipynb     # Main research notebook
├── social_media_engine.py          # Core social media posting engine  
├── notebook_to_social.py           # Notebook data extraction
├── notion_page_generator.py        # NEW: Comprehensive Notion landing pages
├── graphql_resolvers.py            # NEW: GraphQL API integration
├── qxr_main.py                     # Main execution script
├── test_social_integration.py      # Comprehensive test suite
└── README.md                       # This documentation
```

**NEW: GraphQL API Integration**
- `@graphQL.ynl` - Complete GraphQL schema definition
- `@GraphQL` - GraphQL configuration file
- `graphql_resolvers.py` - COMBSEC authenticated resolvers

## Usage

### Quick Start

1. **Run the integration**:
   ```bash
   cd QXR
   python3 qxr_main.py
   ```

2. **Generated output files will be saved to `/tmp/qxr_social_posts/`**:
   - `qxr_social_posts_TIMESTAMP.md` - Master file with all posts
   - `linkedin_TIMESTAMP.txt` - LinkedIn-specific content
   - `twitter_TIMESTAMP.txt` - Twitter-specific content
   - `github_TIMESTAMP.txt` - GitHub-specific content
   - `notion_TIMESTAMP.txt` - **Comprehensive Backtest Sim Landing Page** (Markdown format)
   - `qxr_backtest_sim_landing_page_TIMESTAMP.json` - **Notion API specification** for programmatic creation

3. **Enhanced Notion Workflow**:
   - **For Landing Pages**: Import the comprehensive markdown directly into Notion
   - **For API Integration**: Use the JSON specification for automated page creation
   - **Allocator Setup**: Configure shared access permissions as specified in the landing page
   - **Security Verification**: Ensure COMBSEC authentication before sharing with allocators

4. **Manual posting workflow**:
   - Open the master markdown file
   - Copy content for each platform
   - Login to social media platforms manually
   - **For Notion**: Import landing page markdown or use API specification
   - Paste and publish content

### Advanced Usage

```bash
# Show help
python3 qxr_main.py --help

# Run tests
python3 qxr_main.py --test

# Demo GraphQL API integration
python3 qxr_main.py --graphql

# Test individual components
python3 social_media_engine.py      # Test engine
python3 notebook_to_social.py       # Test notebook processing
python3 graphql_resolvers.py        # Test GraphQL resolvers
python3 test_social_integration.py  # Run full test suite
```

### GraphQL API Integration

The QXR system now includes a comprehensive GraphQL API for programmatic access:

**Schema Definition**: `@graphQL.ynl`
**Configuration**: `@GraphQL`
**Resolvers**: `QXR/graphql_resolvers.py`

#### Key GraphQL Operations:

```graphql
# Generate COMBSEC authentication key
mutation {
  generateCombsecKey(firmId: "YOURFIRM") {
    sessionKey
    truncatedKey
    verified
    generatedAt
  }
}

# Extract research metrics from notebook
query {
  extractNotebookMetrics(notebookPath: "/path/to/notebook.ipynb") {
    signals
    opportunities  
    signalStrength
    priceRange
    maxLiquidity
    strategy
    timeframe
  }
}

# Generate social media posts package
mutation {
  generateSocialMediaPackage(
    researchData: {
      signals: 45
      opportunities: 8
      signalStrength: 1.247
      priceRange: [3420, 3580]
      maxLiquidity: 12500000
      strategy: "ETH Statistical Arbitrage"
      timeframe: "24h"
    }
    options: {
      targetPlatforms: ["linkedin", "twitter", "notion"]
      firmId: "YOURFIRM"
      includeNotionLanding: true
    }
    auth: {
      sessionKey: "🌐-HEXKEY-TIMESTAMP-FIRMID"
      firmId: "YOURFIRM"
    }
  ) {
    masterFile
    posts {
      platform
      content
      hashtags
      combsecKey
      generatedAt
    }
    notionLandingPage {
      specFile
      markdownContent
      apiSpec
    }
    instructions
  }
}

# Monitor system health
query {
  systemHealth {
    status
    combsecActive
    notionIntegration
    socialMediaEngine
  }
}
```

## Research Notebook Integration

The system extracts key metrics from `ETHLIQENGDOTIPYNBNTBK.ipynb`:

- **Statistical Arbitrage Signals**: Buy/sell opportunity counts
- **Signal Strength**: Average signal confidence scores
- **ETH Price Analysis**: Price ranges and market data
- **Liquidity Metrics**: Market liquidity depth measurements
- **Performance Statistics**: Strategy effectiveness data

### Supported Data Patterns

The notebook processor recognizes:
- Output text patterns: "Total signals: 45", "Recent opportunities: 8"
- Variable assignments: `signals = 45`, `signal_strength = 1.247`
- Price ranges: "$3420 - $3580"
- Performance metrics in printed outputs

## Platform-Specific Features

### LinkedIn
- **Max Length**: 3,000 characters
- **Format**: Professional tone with full analysis
- **Features**: Hashtags, detailed metrics, COMBSEC verification

### Twitter  
- **Max Length**: 280 characters
- **Format**: Concise summary with key metrics
- **Features**: Smart truncation, thread suggestions for long content

### GitHub
- **Max Length**: 5,000 characters  
- **Format**: Technical focus with code references
- **Features**: Repository links, technical documentation

### Notion
- **Max Length**: 10,000 characters
- **Format**: Detailed analysis with embedded data
- **Features**: Rich content, comprehensive documentation

## COMBSEC Integration

### Authentication Flow

1. **Key Generation**: Uses ACTNEWWORLDODOR EmojiCombsecGenerator with "QXR" firm ID
2. **Session Authentication**: Sets environment variable `QXR_SOCIAL_COMBSEC_KEY`
3. **Post Verification**: Includes truncated COMBSEC key in all posts
4. **Security**: Full keys stored privately, only prefixes shown publicly

### Example COMBSEC Key Format
```
🌐-B63A58BA9C497480-1758665214-QXR
```

- `🌐`: Globe emoji (U+1F310)
- `B63A58BA9C497480`: 16-character hex key
- `1758665214`: Unix timestamp
- `QXR`: Firm identifier

## Sample Output

### LinkedIn Post Example
```
🌐 QXR ETH Liquidity Research Update

📊 Latest Statistical Arbitrage Analysis:
• Total signals: 45
• Recent opportunities: 8
• Avg signal strength: 1.247

💡 ETH Price Range: $3420 - $3580
📈 Max Liquidity: $12,500,000

🔐 Verified with COMBSEC: 🌐-B63A58BA9C497480-1...
Generated: 2025-09-23 22:06:54

#ETH #DeFi #QuantResearch #StatArb #CryptoAnalysis #QXR #COMBSEC
```

## Testing

The system includes comprehensive tests:

```bash
# Run all tests
python3 test_social_integration.py

# Test results (16 tests):
# ✅ Social Media Engine Tests (8/8)
# ✅ Notebook Processor Tests (6/6)  
# ✅ Integration Tests (2/2)
```

### Test Coverage
- COMBSEC authentication and key generation
- Platform-specific content formatting
- Notebook data extraction and parsing
- End-to-end workflow validation
- Error handling and edge cases

## Security Considerations

1. **COMBSEC Keys**: Never share full keys publicly
2. **Manual Posting**: No automatic API posting for security
3. **Environment Variables**: Session keys stored in environment
4. **Key Truncation**: Only show first 20 characters in posts
5. **Private Logs**: Full session data kept in private files

## Integration with ACTNEWWORLDODOR

The QXR system extends the existing ACTNEWWORLDODOR infrastructure:

- **Inherits COMBSEC**: Uses existing emoji-based key system
- **Extends Protocols**: Adds social media integration protocols  
- **Maintains Security**: Follows established security patterns
- **Consistent Architecture**: Uses same patterns as main system

## Troubleshooting

### Common Issues

1. **Notebook Not Found**:
   ```
   ❌ Error: Notebook not found at ETHLIQENGDOTIPYNBNTBK.ipynb
   ```
   - Ensure the notebook file exists in the QXR directory

2. **No Research Data**:
   ```
   ❌ Failed to extract research data from notebook
   ```
   - Check that the notebook has executed cells with outputs
   - Verify data patterns match expected formats

3. **Import Errors**:
   ```
   ModuleNotFoundError: No module named 'social_media_engine'
   ```
   - Run scripts from the QXR directory
   - Ensure all Python files are in the same directory

### Debug Mode

Set environment variables for debugging:
```bash
export QXR_DEBUG=1
export QXR_VERBOSE=1
python3 qxr_main.py
```

## Contributing

To extend the system:

1. **Add New Platforms**: Update `SocialPlatform` definitions
2. **Enhance Parsing**: Extend `_parse_output_text()` patterns  
3. **Custom Formatting**: Modify `format_for_platform()` logic
4. **Additional Tests**: Add test cases to `test_social_integration.py`

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│ ETHLIQENGDO...  │    │ NotebookProcessor│    │ SocialMediaEngine│
│ .ipynb          │───▶│                  │───▶│                 │
│ (Research Data) │    │ (Data Extract)   │    │ (Post Generation)│
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                         │
                                                         ▼
                                               ┌─────────────────┐
                                               │ Manual Posting  │
                                               │ Files Generated │
                                               │ • LinkedIn      │
                                               │ • Twitter       │
                                               │ • GitHub        │
                                               │ • Notion        │
                                               └─────────────────┘
```

The system provides a secure, efficient bridge between quantitative research outputs and social media engagement, maintaining the high security standards of the ACTNEWWORLDODOR framework while enabling broad dissemination of research insights.