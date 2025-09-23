# Repository-Wide Naming Conventions and File Organization Standards

## Overview
This document establishes unified naming conventions and file organization standards for the OpenAIDeepSeekAIChatGPTOpenSourceCollaborationTransparency repository.

## Core Principles

### 1. File Extension Membership
All files MUST have appropriate extensions that indicate their type and purpose:

#### Data Files (Flat Files)
- `.csv` - Comma-separated values
- `.xml` - XML data/configuration
- `.xlsx` - Excel spreadsheet
- `.json` - JSON data
- `.yaml/.yml` - YAML configuration
- `.txt` - Plain text files

#### Documentation Files
- `.md` - Markdown documentation
- `.rst` - reStructuredText
- `.txt` - Plain text documentation

#### Executable Files
- `.py` - Python scripts (with shebang `#!/usr/bin/env python3`)
- `.sh` - Shell scripts (with shebang `#!/bin/bash`)
- `.js` - JavaScript files
- `.ts` - TypeScript files

### 2. Naming Convention Rules

#### File Names
- Use lowercase letters only
- Use underscores (_) to separate words
- Be descriptive and specific
- Avoid spaces, special characters (!@#$%^&*), and numbers at the start
- Keep names concise but clear

#### Examples
- ✅ `user_data.csv`
- ✅ `config_settings.xml`
- ✅ `sample_template.xlsx`
- ✅ `file_validator.py`
- ❌ `ODOMETERFAKE!`
- ❌ `Screenshot 2025-09-22 221121.png`
- ❌ `File1`
- ❌ `data`

#### Directory Names
- Follow same rules as file names
- Use descriptive names that indicate purpose
- Avoid excessive nesting (max 3-4 levels)
- Use consistent patterns across the repository

### 3. Executable Files Standards

#### Script Requirements
1. **Shebang Lines**: All executable scripts must include proper shebang
   ```bash
   #!/bin/bash          # For shell scripts
   #!/usr/bin/env python3   # For Python scripts
   #!/usr/bin/env node      # For Node.js scripts
   ```

2. **File Permissions**: Set executable permissions with `chmod +x`

3. **Documentation**: Include header comments explaining purpose

4. **Error Handling**: Implement proper error handling and exit codes

### 4. Flat File Alternatives

#### Instead of Basic Text Files
- **Configuration**: Use `.yaml`, `.json`, or `.xml` instead of plain text
- **Data**: Use structured formats like `.csv`, `.json`, or database files
- **Documentation**: Use `.md` or `.rst` for better formatting
- **Logs**: Use structured logging formats

#### Database Alternatives
- **SQLite**: `.db` or `.sqlite` for embedded databases
- **JSON Lines**: `.jsonl` for streaming data
- **Parquet**: `.parquet` for analytical data

### 5. Implementation Strategy

#### Phase 1: Fix Critical Issues
- [ ] Rename files without extensions
- [ ] Add proper extensions to all files
- [ ] Fix files with spaces or special characters
- [ ] Add shebang lines to scripts

#### Phase 2: Standardization
- [ ] Implement consistent naming across all directories
- [ ] Create template files for common formats
- [ ] Add validation scripts
- [ ] Update documentation

#### Phase 3: Enhancement
- [ ] Migrate to better file formats where appropriate
- [ ] Implement automated validation
- [ ] Create style guides for new files
- [ ] Set up CI/CD checks for naming conventions

### 6. File Categories and Organization

#### Project Root
```
├── .gitignore              # Git ignore patterns
├── README.md              # Main project documentation
├── SECURITY.md           # Security documentation
├── ACTNEWWORLDODOR/      # Specific feature directory
└── [other_directories]/   # Follow same patterns
```

#### ACTNEWWORLDODOR Directory Structure
```
ACTNEWWORLDODOR/
├── README.md                    # Directory documentation
├── sample_data.csv              # Sample CSV file
├── sample_config.xml            # Sample XML configuration
├── data_template_xlsx_spec.md   # Excel template specification
├── file_organization_utility.py # Python validation script
├── validate_files.sh            # Shell validation script
├── odometerfake_references.txt  # Renamed reference file
└── [screenshots]/               # Organized screenshots
```

### 7. Validation and Compliance

#### Automated Checks
- File extension validation
- Naming convention compliance
- Executable file shebang verification
- Documentation completeness

#### Tools Provided
- `file_organization_utility.py` - Python-based validation
- `validate_files.sh` - Shell-based validation
- `.gitignore` patterns for proper categorization

### 8. Migration Guidelines

#### Existing Files
1. Audit all files without extensions
2. Determine appropriate file types
3. Rename with proper extensions
4. Update any references to old names
5. Test functionality after changes

#### New Files
1. Always include appropriate extensions
2. Follow naming conventions from creation
3. Add proper documentation headers
4. Set correct permissions for executables

### 9. Maintenance

#### Regular Tasks
- Run validation scripts monthly
- Check for new files without proper extensions
- Update documentation as needed
- Review and improve file organization

#### Quality Gates
- Pre-commit hooks for naming validation
- CI/CD checks for file standards
- Code review requirements for new files
- Documentation updates for changes

## Summary

This standardization addresses the key issues mentioned in ACTNEWWORLDODOR:
- ✅ Non-executing files now have proper extensions and shebangs
- ✅ Flat files (.xml, .csv, .xlsx) have proper dot membership
- ✅ Unified naming conventions established
- ✅ Alternatives to flat files documented and implemented
- ✅ Validation tools created for ongoing compliance