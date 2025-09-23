#!/bin/bash

# GitHub App Installation Access Token Script
# This script creates an installation access token for a GitHub App
# Based on the curl command from the problem statement

set -e  # Exit on any error

# Function to display usage
show_usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Create a GitHub App installation access token"
    echo ""
    echo "OPTIONS:"
    echo "  -i, --installation-id ID    GitHub App installation ID (required)"
    echo "  -j, --jwt TOKEN             JWT token for authentication (required)"
    echo "  -r, --repository-ids IDS    Comma-separated list of repository IDs (default: 321)"
    echo "  -p, --permissions JSON      JSON string of permissions (default: deployments:write)"
    echo "  -h, --help                  Show this help message"
    echo ""
    echo "ENVIRONMENT VARIABLES:"
    echo "  GITHUB_INSTALLATION_ID      GitHub App installation ID"
    echo "  GITHUB_JWT_TOKEN            JWT token for authentication"
    echo ""
    echo "EXAMPLES:"
    echo "  $0 -i 123456 -j eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9..."
    echo "  $0 --installation-id 123456 --jwt eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9... --repository-ids 321,456"
}

# Default values
INSTALLATION_ID="${GITHUB_INSTALLATION_ID:-}"
JWT_TOKEN="${GITHUB_JWT_TOKEN:-}"
REPOSITORY_IDS="321"
PERMISSIONS='{"deployments": "write"}'

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -i|--installation-id)
            INSTALLATION_ID="$2"
            shift 2
            ;;
        -j|--jwt)
            JWT_TOKEN="$2"
            shift 2
            ;;
        -r|--repository-ids)
            REPOSITORY_IDS="$2"
            shift 2
            ;;
        -p|--permissions)
            PERMISSIONS="$2"
            shift 2
            ;;
        -h|--help)
            show_usage
            exit 0
            ;;
        *)
            echo "Error: Unknown option $1"
            show_usage
            exit 1
            ;;
    esac
done

# Validate required parameters
if [[ -z "$INSTALLATION_ID" ]]; then
    echo "Error: Installation ID is required. Use -i/--installation-id or set GITHUB_INSTALLATION_ID environment variable."
    show_usage
    exit 1
fi

if [[ -z "$JWT_TOKEN" ]]; then
    echo "Error: JWT token is required. Use -j/--jwt or set GITHUB_JWT_TOKEN environment variable."
    show_usage
    exit 1
fi

# Convert repository IDs to JSON array format
IFS=',' read -ra REPO_ARRAY <<< "$REPOSITORY_IDS"
REPO_JSON="["
for i in "${!REPO_ARRAY[@]}"; do
    if [[ $i -gt 0 ]]; then
        REPO_JSON+=","
    fi
    REPO_JSON+="${REPO_ARRAY[i]}"
done
REPO_JSON+="]"

# Build the JSON payload
JSON_PAYLOAD=$(cat <<EOF
{
  "repository_ids": $REPO_JSON,
  "permissions": $PERMISSIONS
}
EOF
)

echo "Creating GitHub App installation access token..."
echo "Installation ID: $INSTALLATION_ID"
echo "Repository IDs: $REPO_JSON"
echo "Permissions: $PERMISSIONS"
echo ""

# Execute the curl command as specified in the problem statement
curl --request POST \
     --url "https://api.github.com/app/installations/$INSTALLATION_ID/access_tokens" \
     --header "Accept: application/vnd.github+json" \
     --header "Authorization: Bearer $JWT_TOKEN" \
     --header "Content-Type: application/json" \
     --data "$JSON_PAYLOAD"

echo ""
echo "Access token request completed."