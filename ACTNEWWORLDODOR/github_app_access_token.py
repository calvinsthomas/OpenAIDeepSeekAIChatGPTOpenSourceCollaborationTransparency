#!/usr/bin/env python3
"""
GitHub App Installation Access Token Script

This script creates an installation access token for a GitHub App
Based on the curl command from the problem statement
"""

import argparse
import json
import os
import sys
import requests


def create_access_token(installation_id, jwt_token, repository_ids=None, permissions=None):
    """
    Create a GitHub App installation access token
    
    Args:
        installation_id (str): GitHub App installation ID
        jwt_token (str): JWT token for authentication
        repository_ids (list): List of repository IDs (default: [321])
        permissions (dict): Permissions dictionary (default: {"deployments": "write"})
    
    Returns:
        dict: API response
    """
    if repository_ids is None:
        repository_ids = [321]
    
    if permissions is None:
        permissions = {"deployments": "write"}
    
    url = f"https://api.github.com/app/installations/{installation_id}/access_tokens"
    
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {jwt_token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "repository_ids": repository_ids,
        "permissions": permissions
    }
    
    print(f"Creating GitHub App installation access token...")
    print(f"Installation ID: {installation_id}")
    print(f"Repository IDs: {repository_ids}")
    print(f"Permissions: {permissions}")
    print()
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: Failed to create access token: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response status: {e.response.status_code}")
            print(f"Response body: {e.response.text}")
        sys.exit(1)


def parse_repository_ids(repo_ids_str):
    """Parse comma-separated repository IDs into a list of integers"""
    if not repo_ids_str:
        return [321]
    
    try:
        return [int(repo_id.strip()) for repo_id in repo_ids_str.split(',')]
    except ValueError as e:
        print(f"Error: Invalid repository ID format: {e}")
        sys.exit(1)


def parse_permissions(permissions_str):
    """Parse JSON permissions string into a dictionary"""
    if not permissions_str:
        return {"deployments": "write"}
    
    try:
        return json.loads(permissions_str)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format for permissions: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Create a GitHub App installation access token",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Environment Variables:
  GITHUB_INSTALLATION_ID      GitHub App installation ID
  GITHUB_JWT_TOKEN            JWT token for authentication

Examples:
  %(prog)s -i 123456 -j eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9...
  %(prog)s --installation-id 123456 --jwt eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9... --repository-ids 321,456
        """
    )
    
    parser.add_argument(
        '-i', '--installation-id',
        default=os.environ.get('GITHUB_INSTALLATION_ID'),
        required=not os.environ.get('GITHUB_INSTALLATION_ID'),
        help='GitHub App installation ID (required)'
    )
    
    parser.add_argument(
        '-j', '--jwt',
        default=os.environ.get('GITHUB_JWT_TOKEN'),
        required=not os.environ.get('GITHUB_JWT_TOKEN'),
        help='JWT token for authentication (required)'
    )
    
    parser.add_argument(
        '-r', '--repository-ids',
        default='321',
        help='Comma-separated list of repository IDs (default: 321)'
    )
    
    parser.add_argument(
        '-p', '--permissions',
        default='{"deployments": "write"}',
        help='JSON string of permissions (default: {"deployments": "write"})'
    )
    
    args = parser.parse_args()
    
    # Validate required parameters
    if not args.installation_id:
        print("Error: Installation ID is required. Use -i/--installation-id or set GITHUB_INSTALLATION_ID environment variable.")
        sys.exit(1)
    
    if not args.jwt:
        print("Error: JWT token is required. Use -j/--jwt or set GITHUB_JWT_TOKEN environment variable.")
        sys.exit(1)
    
    # Parse arguments
    repository_ids = parse_repository_ids(args.repository_ids)
    permissions = parse_permissions(args.permissions)
    
    # Create access token
    result = create_access_token(
        args.installation_id,
        args.jwt,
        repository_ids,
        permissions
    )
    
    print("Access token created successfully!")
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()