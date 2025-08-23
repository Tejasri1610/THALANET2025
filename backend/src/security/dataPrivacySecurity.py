#!/usr/bin/env python3
"""
Data Privacy & Security Module for ThalaNet Emergency Blood Management Platform
Implements encryption, data masking, and security utilities for sensitive information
"""

import hashlib
import hmac
import secrets
import base64
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any, Union
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import re
import pandas as pd
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataPrivacySecurity:
    def __init__(self, config: Dict = None):
        """
        Initialize the data privacy and security module
        
        Args:
            config: Configuration dictionary with security settings
        """
        self.config = config or self._get_default_config()
        
        # Initialize encryption key
        self.encryption_key = self._generate_or_load_encryption_key()
        self.cipher_suite = Fernet(self.encryption_key)
        
        # Data masking patterns
        self.masking_patterns = self._initialize_masking_patterns()
        
        # Security audit log
        self.security_audit_log = []
        
        logger.info("Data Privacy & Security module initialized")
    
    def _get_default_config(self) -> Dict:
        """Get default security configuration"""
        return {
            'encryption_algorithm': 'AES-256',
            'key_derivation_rounds': 100000,
            'salt_length': 32,
            'hash_algorithm': 'sha256',
            'session_timeout_minutes': 30,
            'max_login_attempts': 5,
            'password_min_length': 8,
            'enable_audit_logging': True,
            'data_retention_days': 365,
            'pii_fields': [
                'name', 'email', 'phone', 'contact_number', 'address',
                'aadhar_number', 'pan_number', 'passport_number'
            ]
        }
    
    def _generate_or_load_encryption_key(self) -> bytes:
        """Generate or load encryption key"""
        try:
            # In production, load from secure key management system
            # For development, generate a new key
            key = Fernet.generate_key()
            logger.info("Generated new encryption key")
            return key
        except Exception as e:
            logger.error(f"Error generating encryption key: {e}")
            # Fallback to a default key (NOT for production)
            return b'default_key_for_development_only_change_in_production_'
    
    def _initialize_masking_patterns(self) -> Dict[str, Dict]:
        """Initialize data masking patterns for different field types"""
        return {
            'phone_number': {
                'pattern': r'(\d{3})(\d{3})(\d{4})',
                'replacement': r'\1***\3',
                'description': 'Mask middle 3 digits of phone number'
            },
            'email': {
                'pattern': r'(.{2})(.*)(@.*)',
                'replacement': r'\1***\3',
                'description': 'Mask characters between first 2 and @ symbol'
            },
            'name': {
                'pattern': r'^(\w)(\w*)(\w)$',
                'replacement': r'\1***\3',
                'description': 'Mask middle characters of name'
            },
            'aadhar_number': {
                'pattern': r'(\d{4})(\d{4})(\d{4})',
                'replacement': r'\1****\3',
                'description': 'Mask middle 4 digits of Aadhar number'
            },
            'pan_number': {
                'pattern': r'(\w{5})(\d{4})(\w)',
                'replacement': r'\1****\3',
                'description': 'Mask middle 4 digits of PAN number'
            },
            'address': {
                'pattern': r'^(.{10})(.*)(.{10})$',
                'replacement': r'\1***\3',
                'description': 'Mask middle portion of address'
            }
        }
    
    def encrypt_sensitive_data(self, data: str) -> str:
        """
        Encrypt sensitive data using Fernet encryption
        
        Args:
            data: Plain text data to encrypt
            
        Returns:
            Encrypted data as base64 string
        """
        try:
            if not isinstance(data, str):
                data = str(data)
            
            encrypted_data = self.cipher_suite.encrypt(data.encode('utf-8'))
            return base64.b64encode(encrypted_data).decode('utf-8')
        
        except Exception as e:
            logger.error(f"Error encrypting data: {e}")
            return data  # Return original data if encryption fails
    
    def decrypt_sensitive_data(self, encrypted_data: str) -> str:
        """
        Decrypt encrypted data
        
        Args:
            encrypted_data: Base64 encoded encrypted data
            
        Returns:
            Decrypted plain text data
        """
        try:
            encrypted_bytes = base64.b64decode(encrypted_data.encode('utf-8'))
            decrypted_data = self.cipher_suite.decrypt(encrypted_bytes)
            return decrypted_data.decode('utf-8')
        
        except Exception as e:
            logger.error(f"Error decrypting data: {e}")
            return encrypted_data  # Return original data if decryption fails
    
    def hash_password(self, password: str, salt: str = None) -> Tuple[str, str]:
        """
        Hash password using PBKDF2 with salt
        
        Args:
            password: Plain text password
            salt: Optional salt (generated if not provided)
            
        Returns:
            Tuple of (hashed_password, salt)
        """
        try:
            if salt is None:
                salt = secrets.token_hex(self.config['salt_length'] // 2)
            
            # Convert password and salt to bytes
            password_bytes = password.encode('utf-8')
            salt_bytes = salt.encode('utf-8')
            
            # Generate key using PBKDF2
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt_bytes,
                iterations=self.config['key_derivation_rounds']
            )
            
            key = kdf.derive(password_bytes)
            hashed_password = base64.b64encode(key).decode('utf-8')
            
            return hashed_password, salt
        
        except Exception as e:
            logger.error(f"Error hashing password: {e}")
            # Fallback to simple hash (NOT for production)
            return hashlib.sha256(password.encode()).hexdigest(), salt or 'fallback_salt'
    
    def verify_password(self, password: str, hashed_password: str, salt: str) -> bool:
        """
        Verify password against stored hash
        
        Args:
            password: Plain text password to verify
            hashed_password: Stored hashed password
            salt: Salt used for hashing
            
        Returns:
            True if password matches, False otherwise
        """
        try:
            # Hash the provided password with the same salt
            computed_hash, _ = self.hash_password(password, salt)
            return hmac.compare_digest(computed_hash, hashed_password)
        
        except Exception as e:
            logger.error(f"Error verifying password: {e}")
            return False
    
    def mask_pii_data(self, data: str, field_type: str) -> str:
        """
        Mask personally identifiable information
        
        Args:
            data: Data to mask
            field_type: Type of field for masking pattern
            
        Returns:
            Masked data
        """
        try:
            if not data or not isinstance(data, str):
                return data
            
            if field_type in self.masking_patterns:
                pattern_info = self.masking_patterns[field_type]
                pattern = pattern_info['pattern']
                replacement = pattern_info['replacement']
                
                masked_data = re.sub(pattern, replacement, data)
                logger.info(f"Masked {field_type} data: {data[:10]}... -> {masked_data[:10]}...")
                return masked_data
            
            return data
        
        except Exception as e:
            logger.error(f"Error masking {field_type} data: {e}")
            return data
    
    def mask_dataframe_pii(self, df: pd.DataFrame, pii_columns: List[str] = None) -> pd.DataFrame:
        """
        Mask PII columns in a pandas DataFrame
        
        Args:
            df: DataFrame to mask
            pii_columns: List of PII column names (uses default if None)
            
        Returns:
            DataFrame with masked PII data
        """
        try:
            if pii_columns is None:
                pii_columns = self.config['pii_fields']
            
            masked_df = df.copy()
            
            for column in pii_columns:
                if column in masked_df.columns:
                    # Determine field type for masking
                    field_type = self._detect_field_type(column, masked_df[column].iloc[0] if len(masked_df) > 0 else '')
                    
                    if field_type:
                        masked_df[column] = masked_df[column].apply(
                            lambda x: self.mask_pii_data(str(x), field_type)
                        )
            
            logger.info(f"Masked PII data in {len(pii_columns)} columns")
            return masked_df
        
        except Exception as e:
            logger.error(f"Error masking DataFrame PII: {e}")
            return df
    
    def _detect_field_type(self, column_name: str, sample_value: str) -> Optional[str]:
        """Detect field type based on column name and sample value"""
        column_lower = column_name.lower()
        sample_str = str(sample_value).lower()
        
        # Phone number detection
        if any(word in column_lower for word in ['phone', 'mobile', 'contact', 'number']):
            if re.match(r'^\+?[\d\s\-\(\)]+$', sample_str):
                return 'phone_number'
        
        # Email detection
        if 'email' in column_lower or '@' in sample_str:
            return 'email'
        
        # Name detection
        if any(word in column_lower for word in ['name', 'first', 'last', 'full']):
            if re.match(r'^[a-zA-Z\s]+$', sample_str):
                return 'name'
        
        # Aadhar number detection
        if 'aadhar' in column_lower or 'uid' in column_lower:
            if re.match(r'^\d{12}$', sample_str):
                return 'aadhar_number'
        
        # PAN number detection
        if 'pan' in column_lower:
            if re.match(r'^[A-Z]{5}\d{4}[A-Z]$', sample_str):
                return 'pan_number'
        
        # Address detection
        if any(word in column_lower for word in ['address', 'location', 'street', 'city']):
            if len(sample_str) > 20:
                return 'address'
        
        return None
    
    def generate_secure_token(self, length: int = 32) -> str:
        """
        Generate a cryptographically secure random token
        
        Args:
            length: Length of token in bytes
            
        Returns:
            Secure random token
        """
        try:
            token = secrets.token_urlsafe(length)
            logger.info(f"Generated secure token of length {length}")
            return token
        except Exception as e:
            logger.error(f"Error generating secure token: {e}")
            # Fallback to less secure method
            return hashlib.sha256(str(datetime.now()).encode()).hexdigest()[:length]
    
    def validate_password_strength(self, password: str) -> Dict[str, Any]:
        """
        Validate password strength requirements
        
        Args:
            password: Password to validate
            
        Returns:
            Dictionary with validation results
        """
        validation_result = {
            'is_valid': True,
            'errors': [],
            'strength_score': 0,
            'suggestions': []
        }
        
        try:
            # Check minimum length
            if len(password) < self.config['password_min_length']:
                validation_result['is_valid'] = False
                validation_result['errors'].append(f"Password must be at least {self.config['password_min_length']} characters long")
            
            # Check for uppercase letters
            if not re.search(r'[A-Z]', password):
                validation_result['strength_score'] += 1
                validation_result['suggestions'].append("Add uppercase letters")
            
            # Check for lowercase letters
            if not re.search(r'[a-z]', password):
                validation_result['strength_score'] += 1
                validation_result['suggestions'].append("Add lowercase letters")
            
            # Check for numbers
            if not re.search(r'\d', password):
                validation_result['strength_score'] += 1
                validation_result['suggestions'].append("Add numbers")
            
            # Check for special characters
            if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
                validation_result['strength_score'] += 1
                validation_result['suggestions'].append("Add special characters")
            
            # Calculate strength score (0-4, higher is better)
            validation_result['strength_score'] = 4 - validation_result['strength_score']
            
            # Additional validation rules
            if len(password) < 8:
                validation_result['strength_score'] = max(0, validation_result['strength_score'] - 1)
            elif len(password) >= 12:
                validation_result['strength_score'] = min(4, validation_result['strength_score'] + 1)
            
            # Password is too weak if score is 0
            if validation_result['strength_score'] == 0:
                validation_result['is_valid'] = False
                validation_result['errors'].append("Password is too weak")
            
            return validation_result
        
        except Exception as e:
            logger.error(f"Error validating password strength: {e}")
            validation_result['is_valid'] = False
            validation_result['errors'].append("Error validating password")
            return validation_result
    
    def sanitize_input(self, input_data: str) -> str:
        """
        Sanitize user input to prevent injection attacks
        
        Args:
            input_data: Raw input data
            
        Returns:
            Sanitized input data
        """
        try:
            if not input_data:
                return input_data
            
            # Remove potentially dangerous characters
            sanitized = re.sub(r'[<>"\']', '', input_data)
            
            # Remove script tags
            sanitized = re.sub(r'<script.*?</script>', '', sanitized, flags=re.IGNORECASE | re.DOTALL)
            
            # Remove other potentially dangerous HTML tags
            sanitized = re.sub(r'<[^>]*>', '', sanitized)
            
            # Trim whitespace
            sanitized = sanitized.strip()
            
            return sanitized
        
        except Exception as e:
            logger.error(f"Error sanitizing input: {e}")
            return input_data
    
    def log_security_event(self, event_type: str, user_id: str = None, details: Dict = None):
        """
        Log security events for audit purposes
        
        Args:
            event_type: Type of security event
            user_id: ID of user involved
            details: Additional event details
        """
        try:
            if not self.config['enable_audit_logging']:
                return
            
            event = {
                'timestamp': datetime.now().isoformat(),
                'event_type': event_type,
                'user_id': user_id,
                'details': details or {},
                'ip_address': 'unknown',  # In production, get from request context
                'session_id': 'unknown'   # In production, get from session
            }
            
            self.security_audit_log.append(event)
            
            # Keep only recent events (based on retention policy)
            cutoff_date = datetime.now() - timedelta(days=self.config['data_retention_days'])
            self.security_audit_log = [
                event for event in self.security_audit_log
                if datetime.fromisoformat(event['timestamp']) > cutoff_date
            ]
            
            logger.info(f"Security event logged: {event_type} for user {user_id}")
        
        except Exception as e:
            logger.error(f"Error logging security event: {e}")
    
    def get_security_audit_log(self, 
                              start_date: datetime = None, 
                              end_date: datetime = None,
                              event_type: str = None,
                              user_id: str = None) -> List[Dict]:
        """
        Retrieve security audit log with optional filtering
        
        Args:
            start_date: Start date for filtering
            end_date: End date for filtering
            event_type: Filter by event type
            user_id: Filter by user ID
            
        Returns:
            Filtered security audit log
        """
        try:
            filtered_log = self.security_audit_log.copy()
            
            # Apply filters
            if start_date:
                filtered_log = [
                    event for event in filtered_log
                    if datetime.fromisoformat(event['timestamp']) >= start_date
                ]
            
            if end_date:
                filtered_log = [
                    event for event in filtered_log
                    if datetime.fromisoformat(event['timestamp']) <= end_date
                ]
            
            if event_type:
                filtered_log = [
                    event for event in filtered_log
                    if event['event_type'] == event_type
                ]
            
            if user_id:
                filtered_log = [
                    event for event in filtered_log
                    if event['user_id'] == user_id
                ]
            
            return filtered_log
        
        except Exception as e:
            logger.error(f"Error retrieving security audit log: {e}")
            return []
    
    def export_security_log(self, format: str = 'json', filename: str = None) -> Dict:
        """
        Export security audit log in various formats
        
        Args:
            format: Export format (json, csv)
            filename: Output filename
            
        Returns:
            Dictionary with export data
        """
        try:
            if not filename:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f'security_audit_log_{timestamp}.{format}'
            
            if format.lower() == 'csv':
                # Convert to CSV format
                if self.security_audit_log:
                    csv_data = []
                    headers = list(self.security_audit_log[0].keys())
                    csv_data.append(','.join(headers))
                    
                    for event in self.security_audit_log:
                        row = [str(event.get(header, '')) for header in headers]
                        csv_data.append(','.join(row))
                    
                    return {
                        'status': 'success',
                        'format': 'csv',
                        'data': '\n'.join(csv_data),
                        'filename': filename
                    }
            
            # Default to JSON format
            return {
                'status': 'success',
                'format': 'json',
                'data': self.security_audit_log,
                'filename': filename
            }
        
        except Exception as e:
            logger.error(f"Error exporting security log: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'format': format
            }
    
    def get_security_statistics(self) -> Dict:
        """
        Get security statistics and metrics
        
        Returns:
            Dictionary with security statistics
        """
        try:
            if not self.security_audit_log:
                return {
                    'total_events': 0,
                    'events_by_type': {},
                    'events_by_user': {},
                    'recent_activity': []
                }
            
            # Count events by type
            events_by_type = {}
            events_by_user = {}
            
            for event in self.security_audit_log:
                # Count by event type
                event_type = event['event_type']
                events_by_type[event_type] = events_by_type.get(event_type, 0) + 1
                
                # Count by user
                user_id = event['user_id'] or 'anonymous'
                events_by_user[user_id] = events_by_user.get(user_id, 0) + 1
            
            # Get recent activity (last 10 events)
            recent_activity = sorted(
                self.security_audit_log,
                key=lambda x: x['timestamp'],
                reverse=True
            )[:10]
            
            return {
                'total_events': len(self.security_audit_log),
                'events_by_type': events_by_type,
                'events_by_user': events_by_user,
                'recent_activity': recent_activity,
                'last_updated': datetime.now().isoformat()
            }
        
        except Exception as e:
            logger.error(f"Error getting security statistics: {e}")
            return {'error': str(e)}

def main():
    """Example usage of the data privacy and security module"""
    print("Data Privacy & Security Module")
    print("=" * 50)
    
    # Initialize security module
    security = DataPrivacySecurity()
    
    # Test encryption/decryption
    print("\n1. Testing encryption/decryption...")
    test_data = "sensitive_patient_information"
    encrypted = security.encrypt_sensitive_data(test_data)
    decrypted = security.decrypt_sensitive_data(encrypted)
    print(f"Original: {test_data}")
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")
    print(f"Match: {test_data == decrypted}")
    
    # Test password hashing
    print("\n2. Testing password hashing...")
    password = "MySecurePassword123!"
    hashed, salt = security.hash_password(password)
    is_valid = security.verify_password(password, hashed, salt)
    print(f"Password: {password}")
    print(f"Hashed: {hashed}")
    print(f"Salt: {salt}")
    print(f"Verification: {is_valid}")
    
    # Test password strength validation
    print("\n3. Testing password strength validation...")
    weak_password = "123"
    strong_password = "MySecurePassword123!"
    
    weak_validation = security.validate_password_strength(weak_password)
    strong_validation = security.validate_password_strength(strong_password)
    
    print(f"Weak password validation: {weak_validation}")
    print(f"Strong password validation: {strong_validation}")
    
    # Test data masking
    print("\n4. Testing data masking...")
    test_phone = "+91-9876543210"
    test_email = "john.doe@example.com"
    test_name = "John Doe"
    
    masked_phone = security.mask_pii_data(test_phone, 'phone_number')
    masked_email = security.mask_pii_data(test_email, 'email')
    masked_name = security.mask_pii_data(test_name, 'name')
    
    print(f"Phone: {test_phone} -> {masked_phone}")
    print(f"Email: {test_email} -> {masked_email}")
    print(f"Name: {test_name} -> {masked_name}")
    
    # Test secure token generation
    print("\n5. Testing secure token generation...")
    token = security.generate_secure_token(32)
    print(f"Secure token: {token}")
    
    # Test input sanitization
    print("\n6. Testing input sanitization...")
    malicious_input = "<script>alert('xss')</script>Hello World"
    sanitized = security.sanitize_input(malicious_input)
    print(f"Malicious input: {malicious_input}")
    print(f"Sanitized: {sanitized}")
    
    # Test security logging
    print("\n7. Testing security logging...")
    security.log_security_event('login_attempt', 'user123', {'ip': '192.168.1.1'})
    security.log_security_event('password_change', 'user123', {'method': 'web'})
    security.log_security_event('failed_login', 'user456', {'reason': 'invalid_password'})
    
    # Get security statistics
    stats = security.get_security_statistics()
    print(f"\nSecurity Statistics: {stats}")
    
    print("\nSecurity module testing completed!")

if __name__ == "__main__":
    main()

