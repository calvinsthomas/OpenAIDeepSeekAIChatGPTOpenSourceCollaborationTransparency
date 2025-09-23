# ACTNEWWORLDODOR - File Organization and Naming Conventions

## Overview
This document addresses issues related to non-executing files, file extensions, and unified naming conventions.

## File Extension Standards

### Flat Files with Proper Extensions
- **Data Files**: Always use appropriate extensions
  - `.csv` for comma-separated values
  - `.xml` for XML configuration/data files
  - `.xlsx` for Excel spreadsheets
  - `.json` for JSON data
  - `.txt` for plain text files

### Executable Files
- **Scripts**: Must have proper extensions and shebang lines
  - `.py` for Python scripts
  - `.sh` for shell scripts
  - `.js` for JavaScript files
  - `.ts` for TypeScript files

## Naming Convention Rules

### File Names
1. Use lowercase with underscores for separation
2. Be descriptive and specific
3. Include file extensions
4. Avoid special characters and spaces

### Examples
- ✅ Good: `sample_data.csv`, `config_settings.xml`, `user_data.xlsx`
- ❌ Bad: `ODOMETERFAKE!`, `data`, `File1`

### Directory Structure
- Use consistent naming across all directories
- Avoid excessive nesting
- Use descriptive folder names

## Alternatives to Flat Files

### Structured Alternatives
1. **Database Files**: `.db`, `.sqlite`
2. **Configuration Management**: `.yaml`, `.json`, `.toml`
3. **Documentation**: `.md`, `.rst`
4. **Compressed Archives**: `.zip`, `.tar.gz`

### Best Practices
- Use version control for all files
- Implement proper .gitignore patterns
- Document file purposes and formats
- Use consistent metadata

## File Categories

### Data Files
- Input/output data
- Configuration files
- Templates and schemas

### Documentation
- README files
- API documentation
- User guides

### Executable Content
- Scripts with proper shebangs
- Compiled binaries
- Batch files

## Implementation Guidelines

1. **File Extension Audit**: Ensure all files have proper extensions
2. **Executable Permissions**: Set appropriate permissions for scripts
3. **Shebang Lines**: Add proper shebang lines to executable scripts
4. **Documentation**: Document file purposes and formats
5. **Validation**: Implement file validation and linting

## Examples in This Directory

- `sample_data.csv` - Example CSV with proper structure
- `sample_config.xml` - XML configuration example
- `ODOMETERFAKE_references.txt` - Renamed file with proper extension
- `README.md` - This documentation file