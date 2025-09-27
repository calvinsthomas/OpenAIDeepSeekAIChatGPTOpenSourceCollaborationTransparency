#!/usr/bin/env python3
"""
GitHub Timestamp Integration for COMBSEC System
Enhanced timestamping with GitHub commit and workflow data integration
"""

import os
import time
import json
import hashlib
import subprocess
from datetime import datetime
from typing import Dict, Optional, List, Any
from emoji_combsec_generator import EmojiCombsecGenerator

class GitHubTimestampIntegrator:
    """
    GitHub integration for enhanced COMBSEC key timestamping
    Integrates GitHub commit data, workflow runs, and repository metadata
    """
    
    def __init__(self, firm_id: str = "GITHUB_FIRM"):
        """Initialize GitHub timestamp integrator"""
        self.firm_id = firm_id
        self.combsec_generator = EmojiCombsecGenerator(firm_id)
        
    def get_git_commit_info(self) -> Dict[str, Any]:
        """Get current Git commit information"""
        try:
            # Get current commit hash
            commit_hash = subprocess.check_output(
                ['git', 'rev-parse', 'HEAD'], 
                universal_newlines=True
            ).strip()
            
            # Get commit timestamp
            commit_timestamp = subprocess.check_output(
                ['git', 'show', '-s', '--format=%ct', 'HEAD'],
                universal_newlines=True
            ).strip()
            
            # Get commit author
            commit_author = subprocess.check_output(
                ['git', 'show', '-s', '--format=%an', 'HEAD'],
                universal_newlines=True
            ).strip()
            
            # Get commit message
            commit_message = subprocess.check_output(
                ['git', 'show', '-s', '--format=%s', 'HEAD'],
                universal_newlines=True
            ).strip()
            
            return {
                "commit_hash": commit_hash,
                "commit_timestamp": int(commit_timestamp),
                "commit_author": commit_author,
                "commit_message": commit_message,
                "commit_datetime": datetime.fromtimestamp(int(commit_timestamp)).isoformat()
            }
        except subprocess.CalledProcessError:
            # Fallback if not in a git repository
            return {
                "commit_hash": "NO_GIT_REPO",
                "commit_timestamp": int(time.time()),
                "commit_author": "SYSTEM",
                "commit_message": "No Git repository detected",
                "commit_datetime": datetime.now().isoformat()
            }
    
    def get_github_environment_info(self) -> Dict[str, Any]:
        """Extract GitHub Actions environment information if available"""
        github_env = {}
        
        # Common GitHub Actions environment variables
        github_vars = [
            'GITHUB_ACTOR',
            'GITHUB_REPOSITORY',
            'GITHUB_REF',
            'GITHUB_SHA',
            'GITHUB_WORKFLOW',
            'GITHUB_RUN_ID',
            'GITHUB_RUN_NUMBER',
            'GITHUB_ACTION',
            'GITHUB_EVENT_NAME'
        ]
        
        for var in github_vars:
            github_env[var.lower()] = os.environ.get(var, 'NOT_SET')
        
        return github_env
    
    def generate_github_timestamped_key(self, 
                                      include_commit_data: bool = True,
                                      include_github_env: bool = True) -> Dict[str, Any]:
        """
        Generate a COMBSEC key with GitHub timestamp integration
        
        Args:
            include_commit_data: Include Git commit information
            include_github_env: Include GitHub Actions environment data
            
        Returns:
            Dictionary with key and metadata
        """
        current_timestamp = int(time.time())
        
        # Collect GitHub metadata
        metadata = {
            "generation_timestamp": current_timestamp,
            "generation_datetime": datetime.now().isoformat(),
        }
        
        if include_commit_data:
            metadata["git_info"] = self.get_git_commit_info()
            
        if include_github_env:
            metadata["github_env"] = self.get_github_environment_info()
        
        # Create enhanced entropy from GitHub data
        github_entropy_components = [
            str(current_timestamp),
            metadata.get("git_info", {}).get("commit_hash", ""),
            metadata.get("github_env", {}).get("github_sha", ""),
            metadata.get("github_env", {}).get("github_run_id", ""),
        ]
        
        github_entropy = hashlib.sha256(
            ''.join(github_entropy_components).encode('utf-8')
        ).hexdigest()[:16]
        
        # Generate the COMBSEC key with GitHub-enhanced entropy
        combsec_key = self.combsec_generator.generate_combsec_key(
            timestamp=current_timestamp,
            additional_entropy=github_entropy
        )
        
        return {
            "combsec_key": combsec_key,
            "github_metadata": metadata,
            "entropy_source": "github_enhanced",
            "firm_id": self.firm_id
        }
    
    def validate_github_timestamped_key(self, key_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate a GitHub-timestamped COMBSEC key"""
        if not isinstance(key_data, dict) or "combsec_key" not in key_data:
            return {"valid": False, "error": "Invalid key data format"}
        
        # Validate the base COMBSEC key
        base_validation = self.combsec_generator.validate_combsec_key(
            key_data["combsec_key"]
        )
        
        if not base_validation.get("valid", False):
            return base_validation
        
        # Additional GitHub-specific validation
        github_metadata = key_data.get("github_metadata", {})
        
        validation_result = base_validation.copy()
        validation_result.update({
            "github_enhanced": True,
            "has_git_info": "git_info" in github_metadata,
            "has_github_env": "github_env" in github_metadata,
            "entropy_source": key_data.get("entropy_source", "unknown"),
            "github_metadata": github_metadata
        })
        
        return validation_result
    
    def export_github_key_batch(self, count: int = 10) -> Dict[str, Any]:
        """Generate and export a batch of GitHub-timestamped keys"""
        keys = []
        
        for i in range(count):
            # Add small delay to ensure unique timestamps
            if i > 0:
                time.sleep(0.1)
                
            key_data = self.generate_github_timestamped_key()
            keys.append(key_data)
        
        export_data = {
            "system": "ACTNEWWORLDODOR_GITHUB_COMBSEC",
            "base_emoji": self.combsec_generator.GLOBE_EMOJI,
            "unicode_codepoint": self.combsec_generator.UNICODE_CODEPOINT,
            "firm_id": self.firm_id,
            "export_timestamp": datetime.now().isoformat(),
            "total_keys": len(keys),
            "keys": keys,
            "github_integration": True
        }
        
        return export_data


def generate_github_combsec_key_u1f310(firm_id: str, 
                                      include_commit_data: bool = True,
                                      include_github_env: bool = True) -> str:
    """
    Standardized API function for generating GitHub-enhanced COMBSEC keys
    
    This provides the "ALL MONEY IN! TIMESTAMP ME GH!" functionality
    requested in the problem statement.
    
    Args:
        firm_id: Unique firm identifier
        include_commit_data: Include Git commit information
        include_github_env: Include GitHub Actions environment data
        
    Returns:
        GitHub-enhanced COMBSEC key string
    """
    integrator = GitHubTimestampIntegrator(firm_id)
    key_data = integrator.generate_github_timestamped_key(
        include_commit_data=include_commit_data,
        include_github_env=include_github_env
    )
    
    return key_data["combsec_key"]


if __name__ == "__main__":
    # Demo the GitHub integration functionality
    print("🌐 GitHub-Enhanced COMBSEC Key Generation Demo")
    print("=" * 60)
    
    integrator = GitHubTimestampIntegrator("GITHUB_DEMO_FIRM")
    
    print("🔗 Generating GitHub-enhanced COMBSEC key...")
    key_data = integrator.generate_github_timestamped_key()
    
    print(f"Generated key: {key_data['combsec_key']}")
    print(f"Firm ID: {key_data['firm_id']}")
    print(f"Entropy source: {key_data['entropy_source']}")
    
    print("\nGit information:")
    git_info = key_data["github_metadata"].get("git_info", {})
    for key, value in git_info.items():
        print(f"  {key}: {value}")
    
    print("\nGitHub environment:")
    github_env = key_data["github_metadata"].get("github_env", {})
    for key, value in github_env.items():
        if key in ['github_repository', 'github_actor', 'github_workflow']:
            print(f"  {key}: {value}")
    
    print("\n🧪 Validating the key...")
    validation = integrator.validate_github_timestamped_key(key_data)
    print(f"Valid: {validation['valid']}")
    print(f"GitHub Enhanced: {validation.get('github_enhanced', False)}")
    
    print("\n🎉 GitHub integration demo completed!")