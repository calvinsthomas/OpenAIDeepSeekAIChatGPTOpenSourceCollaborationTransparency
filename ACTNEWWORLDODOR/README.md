# GitHub App Installation Access Token Scripts

This directory contains scripts to create GitHub App installation access tokens using the GitHub API.

## Overview

These scripts implement the curl command for creating GitHub App installation access tokens as specified in the GitHub API documentation. The scripts support both shell and Python environments.

## Files

- `github_app_access_token.sh` - Bash script implementation
- `github_app_access_token.py` - Python script implementation
- `README.md` - This documentation file

## API Call Implementation

Both scripts implement the following GitHub API call:

```bash
curl --request POST \
--url "https://api.github.com/app/installations/INSTALLATION_ID/access_tokens" \
--header "Accept: application/vnd.github+json" \
--header "Authorization: Bearer {jwt}" \
--header "Content-Type: application/json" \
--data \
'{ \
   "repository_ids": [321], \
   "permissions": { \
      "deployments": "write" \
   } \
}'
```

## Usage

### Bash Script

```bash
# Basic usage
./github_app_access_token.sh -i YOUR_INSTALLATION_ID -j YOUR_JWT_TOKEN

# With custom repository IDs and permissions
./github_app_access_token.sh \
  --installation-id 123456 \
  --jwt eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9... \
  --repository-ids 321,456,789 \
  --permissions '{"deployments": "write", "contents": "read"}'

# Using environment variables
export GITHUB_INSTALLATION_ID=123456
export GITHUB_JWT_TOKEN=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9...
./github_app_access_token.sh
```

### Python Script

```bash
# Basic usage
python3 github_app_access_token.py -i YOUR_INSTALLATION_ID -j YOUR_JWT_TOKEN

# With custom repository IDs and permissions
python3 github_app_access_token.py \
  --installation-id 123456 \
  --jwt eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9... \
  --repository-ids 321,456,789 \
  --permissions '{"deployments": "write", "contents": "read"}'

# Using environment variables
export GITHUB_INSTALLATION_ID=123456
export GITHUB_JWT_TOKEN=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9...
python3 github_app_access_token.py
```

## Parameters

### Required Parameters

- **Installation ID** (`-i`, `--installation-id`): The GitHub App installation ID
- **JWT Token** (`-j`, `--jwt`): JWT token for authenticating as the GitHub App

### Optional Parameters

- **Repository IDs** (`-r`, `--repository-ids`): Comma-separated list of repository IDs (default: 321)
- **Permissions** (`-p`, `--permissions`): JSON string of permissions (default: `{"deployments": "write"}`)

## Environment Variables

You can set the following environment variables instead of passing command line arguments:

- `GITHUB_INSTALLATION_ID`: GitHub App installation ID
- `GITHUB_JWT_TOKEN`: JWT token for authentication

## Prerequisites

### For Bash Script
- bash
- curl

### For Python Script
- Python 3.6+
- requests library (`pip install requests`)

## Error Handling

Both scripts include comprehensive error handling:

- Parameter validation
- HTTP error handling
- JSON parsing error handling
- Clear error messages with troubleshooting information

## Examples

### Creating a token for deployments
```bash
./github_app_access_token.sh -i 12345 -j YOUR_JWT_TOKEN
```

### Creating a token for multiple repositories with different permissions
```bash
./github_app_access_token.sh \
  -i 12345 \
  -j YOUR_JWT_TOKEN \
  -r 321,456,789 \
  -p '{"deployments": "write", "contents": "read", "metadata": "read"}'
```

## Output

Both scripts will output:
1. Configuration information (Installation ID, Repository IDs, Permissions)
2. The API response containing the access token and its metadata
3. Success/error messages

Example successful output:
```json
{
  "token": "ghs_16C7e42F292c6912E7710c838347Ae178B4a",
  "expires_at": "2023-12-01T12:00:00Z",
  "permissions": {
    "deployments": "write"
  },
  "repository_selection": "selected"
}
```

## Security Notes

- Keep your JWT tokens secure and never commit them to version control
- Use environment variables for sensitive information when possible
- Access tokens have limited lifespans and should be refreshed as needed
- Follow the principle of least privilege when setting permissions