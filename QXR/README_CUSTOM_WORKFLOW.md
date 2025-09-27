# QXR Custom Workflow Loader

A flexible system for triggering QXR workflows through file-based commands, specifically designed to handle the `.mp4` directory command structure.

## Overview

The Custom Workflow Loader monitors and processes workflow commands stored in file system triggers, enabling automated execution of the main QXR social media integration workflow.

## Problem Statement Addressed

**"On .mp4, loadmymainquantQXRworkflowcustomnow!"**

This implementation provides:
- Detection of command files in the `.mp4` directory
- Automatic parsing and execution of QXR workflow commands
- Comprehensive logging and monitoring capabilities
- Direct execution scripts for immediate workflow triggers

## File Structure

```
.mp4/
├── loadmymainquantQXRworkflowcustomnow!  # Command trigger file
└── run_qxr_workflow.py                   # Direct execution script

QXR/
├── custom_workflow_loader.py             # Main loader implementation
├── qxr_main.py                          # Core QXR workflow
└── README_CUSTOM_WORKFLOW.md            # This file

logs/
└── custom_workflows/                     # Execution logs
    └── custom_workflow_execution_*.json
```

## Usage

### Method 1: Direct Execution from .mp4 Directory
```bash
cd .mp4
python run_qxr_workflow.py
```

### Method 2: Using the Custom Workflow Loader
```bash
# Single execution
python QXR/custom_workflow_loader.py

# Monitor mode (continuous monitoring)
python QXR/custom_workflow_loader.py --monitor

# Help
python QXR/custom_workflow_loader.py --help
```

### Method 3: Standard QXR Workflow
```bash
python QXR/qxr_main.py
```

## Command File Format

The command file `.mp4/loadmymainquantQXRworkflowcustomnow!` contains:
```
loadmymainquantQXRworkflowcustomnow!
```

This command is parsed to:
- **Action**: `load_qxr_workflow`
- **Custom Mode**: `true` (contains "customnow")
- **Execution**: Full QXR social media integration workflow

## Features

### 🔍 Command Processing
- Automatic detection of command files
- Intelligent parsing of workflow commands
- Support for custom execution modes

### 📊 Execution Logging
- Detailed JSON logs for each execution
- Timestamp tracking and performance metrics
- Error handling and success reporting

### 🔄 Monitoring Capabilities
- Continuous file monitoring mode
- Automatic execution on command file changes
- Daemon-style operation for automated workflows

### 🚀 Integration
- Seamless integration with existing QXR workflow
- Bridge-accelerated processing when available
- Full compatibility with enhanced social media engine

## Generated Files

Each execution creates:

1. **Social Media Posts**: `/tmp/qxr_bridge_posts_[timestamp].json`
   - LinkedIn, Twitter, GitHub, Notion content
   - Performance metrics and processing times
   - Bridge version information

2. **Execution Logs**: `logs/custom_workflows/custom_workflow_execution_[timestamp].json`
   - Execution metadata and timing
   - Command processing details
   - Success/failure status

## Workflow Output

The custom workflow loader triggers the full QXR integration which includes:

- ✅ ETHLIQENGDOTIPYNBNTBK notebook processing
- ✅ Statistical arbitrage signal extraction
- ✅ Multi-platform social media content generation
- ✅ COMBSEC authentication integration
- ✅ Notion Backtest Sim Landing Page creation
- ✅ Bridge-accelerated performance optimization

## Security Features

- **COMBSEC Integration**: Secure key authentication
- **Execution Logging**: Complete audit trail
- **Command Validation**: Safe command processing
- **NEWWORLDODOR Context**: Security protocol compliance

## Error Handling

The system handles:
- Missing command files
- Invalid command formats
- Workflow execution failures
- Import/dependency issues
- File system permissions

## Integration with QXR Ecosystem

This custom workflow loader integrates with:
- **QXR Main Workflow** (`qxr_main.py`)
- **Enhanced Social Media Engine** (Bridge integration)
- **Notion Page Generator** (Landing page creation)
- **COMBSEC System** (Authentication)
- **GraphQL Resolvers** (API integration)

## Performance

- **Bridge Acceleration**: 10-100x faster processing when available
- **Minimal Overhead**: Direct command file monitoring
- **Efficient Logging**: JSON-based structured logs
- **Fast Execution**: Sub-second command processing

## Examples

### Successful Execution Log
```json
{
  "execution_id": "custom_1758934479",
  "trigger_source": "/.mp4/loadmymainquantQXRworkflowcustomnow!",
  "command": "loadmymainquantQXRworkflowcustomnow!",
  "processed_command": {
    "action": "load_qxr_workflow",
    "custom": true,
    "timestamp": "2025-09-27T00:54:39.407488"
  },
  "started_at": "2025-09-27T00:54:39.407522",
  "completed_at": "2025-09-27T00:54:39.408667",
  "success": true
}
```

### Generated Social Media Content
```json
{
  "linkedin": {
    "content": "🚀 QXR Research Update: 45 signals detected with 1.247 strength. Performance score: 31.06. 8 opportunities identified in 24h.",
    "performance_score": 31.06,
    "processing_time_ms": 0.02,
    "platform": "linkedin",
    "bridge_version": "QXR Bridge v0.1.0 (Simulation)"
  }
}
```

## Future Enhancements

- **Web Dashboard**: Real-time monitoring interface
- **API Endpoints**: RESTful API for remote execution
- **Scheduled Execution**: Cron-like scheduling capabilities
- **Multiple Command Files**: Support for different workflow types
- **Cloud Integration**: AWS/Azure execution environments