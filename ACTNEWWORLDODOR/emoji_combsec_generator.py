#!/usr/bin/env python3
"""
ACTNEWWORLDODOR - Emoji-Based Combinatoric Security Key Generator
Based on U+1F310 (🌐 Globe/World Emoji)

This module provides the core functionality for generating combinatoric 
security keys using the globe emoji as the foundational element.
"""

import hashlib
import time
import secrets
from typing import Optional, Dict, List
import json
from datetime import datetime

class EmojiCombsecGenerator:
    """
    Emoji-based combinatoric security key generator
    Foundation: U+1F310 (🌐 Globe showing Europe-Africa)
    """
    
    # Core emoji and its properties
    GLOBE_EMOJI = "🌐"
    UNICODE_CODEPOINT = "U+1F310"
    HEX_VALUE = 0x1F310
    UTF8_BYTES = b'\xf0\x9f\x8c\x90'
    
    def __init__(self, firm_id: str = "YOURFIRM"):
        """
        Initialize the COMBSEC key generator
        
        Args:
            firm_id: Unique identifier for the firm/organization
        """
        self.firm_id = firm_id
        self.base_seed = self._generate_base_seed()
        
    def _generate_base_seed(self) -> str:
        """Generate the foundational seed from the globe emoji"""
        # Combine emoji bytes with firm ID
        combined_data = self.UTF8_BYTES + self.firm_id.encode('utf-8')
        
        # Create SHA-256 hash of the combination
        sha256_hash = hashlib.sha256(combined_data).hexdigest()
        
        return sha256_hash
    
    def generate_combsec_key(self, 
                           timestamp: Optional[int] = None,
                           additional_entropy: Optional[str] = None) -> str:
        """
        Generate a COMBSEC key based on U+1F310 globe emoji
        
        Args:
            timestamp: Optional timestamp (defaults to current time)
            additional_entropy: Additional randomness source
            
        Returns:
            Formatted COMBSEC key string in format:
            🌐-[HEXKEY]-[TIMESTAMP]-[FIRMID]
        """
        if timestamp is None:
            timestamp = int(time.time())
            
        # Create the combinatoric components
        components = [
            self.base_seed,
            str(timestamp),
            self.firm_id,
            str(self.HEX_VALUE),
            additional_entropy or secrets.token_hex(8)
        ]
        
        # Generate combinatoric hash
        combined_string = ''.join(components)
        combsec_hash = hashlib.sha256(combined_string.encode('utf-8')).hexdigest()[:16]
        
        # Format the final key
        key = f"{self.GLOBE_EMOJI}-{combsec_hash.upper()}-{timestamp}-{self.firm_id}"
        
        return key
    
    def validate_combsec_key(self, key: str) -> Dict[str, any]:
        """
        Validate and parse a COMBSEC key
        
        Args:
            key: The COMBSEC key to validate
            
        Returns:
            Dictionary with validation results and parsed components
        """
        try:
            parts = key.split('-')
            
            if len(parts) != 4:
                return {"valid": False, "error": "Invalid key format"}
            
            emoji_part, hex_key, timestamp_str, firm_id = parts
            
            # Validate emoji component
            if emoji_part != self.GLOBE_EMOJI:
                return {"valid": False, "error": "Invalid emoji component"}
            
            # Validate hex key format
            if len(hex_key) != 16:
                return {"valid": False, "error": "Invalid hex key length"}
            
            # Parse timestamp
            try:
                timestamp = int(timestamp_str)
                key_datetime = datetime.fromtimestamp(timestamp)
            except ValueError:
                return {"valid": False, "error": "Invalid timestamp"}
            
            return {
                "valid": True,
                "emoji": emoji_part,
                "hex_key": hex_key,
                "timestamp": timestamp,
                "datetime": key_datetime.isoformat(),
                "firm_id": firm_id,
                "unicode_codepoint": self.UNICODE_CODEPOINT
            }
            
        except Exception as e:
            return {"valid": False, "error": f"Parsing error: {str(e)}"}
    
    def generate_key_batch(self, count: int = 10) -> List[str]:
        """
        Generate a batch of COMBSEC keys for bulk operations
        
        Args:
            count: Number of keys to generate
            
        Returns:
            List of COMBSEC keys
        """
        keys = []
        base_time = int(time.time())
        
        for i in range(count):
            # Use sequential timestamps to ensure uniqueness
            timestamp = base_time + i
            entropy = f"batch_{i}_{secrets.token_hex(4)}"
            key = self.generate_combsec_key(timestamp, entropy)
            keys.append(key)
            
        return keys
    
    def export_key_data(self, keys: List[str]) -> Dict[str, any]:
        """
        Export key data in structured format for integration
        
        Args:
            keys: List of COMBSEC keys to export
            
        Returns:
            Structured data dictionary
        """
        export_data = {
            "system": "ACTNEWWORLDODOR_COMBSEC",
            "base_emoji": self.GLOBE_EMOJI,
            "unicode_codepoint": self.UNICODE_CODEPOINT,
            "firm_id": self.firm_id,
            "generation_timestamp": datetime.now().isoformat(),
            "total_keys": len(keys),
            "keys": []
        }
        
        for key in keys:
            validation_result = self.validate_combsec_key(key)
            export_data["keys"].append({
                "key": key,
                "validation": validation_result
            })
            
        return export_data


def generate_combsec_key_u1f310(firm_id: str, timestamp: int = None) -> str:
    """
    Generate COMBSEC key based on U+1F310 globe emoji
    
    This is the standardized API function as specified in the technical design document.
    Provides a risk-free, reliable interface for COMBSEC key generation.
    
    Args:
        firm_id: Unique firm identifier
        timestamp: Optional timestamp (defaults to current time)
    
    Returns:
        Formatted COMBSEC key string in format: 🌐-[HEXKEY]-[TIMESTAMP]-[FIRMID]
    """
    # Create a generator instance for this specific request
    generator = EmojiCombsecGenerator(firm_id)
    
    # Generate and return the key using the existing implementation
    return generator.generate_combsec_key(timestamp=timestamp)


