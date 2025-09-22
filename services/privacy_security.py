"""
Privacy & Security Service for MAYBERRY Medical AI
Implements HIPAA/GDPR compliance and privacy-first architecture
"""

import hashlib
import secrets
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os
from config import settings

class PrivacySecurityService:
    """Advanced privacy and security service for medical data"""
    
    def __init__(self):
        self.encryption_key = self._generate_encryption_key()
        self.cipher_suite = Fernet(self.encryption_key)
        self.privacy_metrics = {
            'local_processing_count': 0,
            'cloud_processing_count': 0,
            'data_encrypted_count': 0,
            'anonymous_sessions': 0
        }
    
    def _generate_encryption_key(self) -> bytes:
        """Generate encryption key for data protection"""
        if settings.DATA_ENCRYPTION_ENABLED:
            # Generate key from password using PBKDF2
            password = settings.SECRET_KEY.encode()
            salt = b'mayberry_medical_salt_2024'
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
            )
            key = base64.urlsafe_b64encode(kdf.derive(password))
            return key
        return b''
    
    def encrypt_sensitive_data(self, data: Any) -> str:
        """Encrypt sensitive medical data"""
        if not settings.DATA_ENCRYPTION_ENABLED:
            return json.dumps(data)
        
        try:
            data_json = json.dumps(data)
            encrypted_data = self.cipher_suite.encrypt(data_json.encode())
            self.privacy_metrics['data_encrypted_count'] += 1
            return base64.urlsafe_b64encode(encrypted_data).decode()
        except Exception as e:
            print(f"Encryption error: {e}")
            return json.dumps(data)
    
    def decrypt_sensitive_data(self, encrypted_data: str) -> Any:
        """Decrypt sensitive medical data"""
        if not settings.DATA_ENCRYPTION_ENABLED:
            return json.loads(encrypted_data)
        
        try:
            decoded_data = base64.urlsafe_b64decode(encrypted_data.encode())
            decrypted_data = self.cipher_suite.decrypt(decoded_data)
            return json.loads(decrypted_data.decode())
        except Exception as e:
            print(f"Decryption error: {e}")
            return {}
    
    def anonymize_user_data(self, user_data: Dict) -> Dict:
        """Anonymize user data for privacy"""
        if not settings.ANONYMOUS_MODE_ENABLED:
            return user_data
        
        anonymized = user_data.copy()
        
        # Remove PII
        pii_fields = ['email', 'phone_number', 'full_name', 'address']
        for field in pii_fields:
            if field in anonymized:
                anonymized[field] = f"anonymous_{hashlib.sha256(str(anonymized[field]).encode()).hexdigest()[:8]}"
        
        # Hash user ID
        if 'user_id' in anonymized:
            anonymized['user_id'] = hashlib.sha256(anonymized['user_id'].encode()).hexdigest()
        
        return anonymized
    
    def generate_anonymous_session(self) -> str:
        """Generate anonymous session ID"""
        if settings.ANONYMOUS_MODE_ENABLED:
            session_id = secrets.token_urlsafe(32)
            self.privacy_metrics['anonymous_sessions'] += 1
            return session_id
        return ""
    
    def track_local_processing(self):
        """Track local processing usage"""
        self.privacy_metrics['local_processing_count'] += 1
    
    def track_cloud_processing(self):
        """Track cloud processing usage"""
        self.privacy_metrics['cloud_processing_count'] += 1
    
    def get_privacy_status(self) -> Dict[str, Any]:
        """Get current privacy and security status"""
        total_processing = (self.privacy_metrics['local_processing_count'] + 
                          self.privacy_metrics['cloud_processing_count'])
        
        local_percentage = 0
        if total_processing > 0:
            local_percentage = (self.privacy_metrics['local_processing_count'] / total_processing) * 100
        
        return {
            'hipaa_compliant': settings.HIPAA_COMPLIANT,
            'gdpr_compliant': settings.GDPR_COMPLIANT,
            'local_processing_enabled': settings.LOCAL_PROCESSING_ENABLED,
            'data_encryption_enabled': settings.DATA_ENCRYPTION_ENABLED,
            'zero_knowledge_architecture': settings.ZERO_KNOWLEDGE_ARCHITECTURE,
            'anonymous_mode_enabled': settings.ANONYMOUS_MODE_ENABLED,
            'local_processing_percentage': round(local_percentage, 1),
            'data_encrypted_count': self.privacy_metrics['data_encrypted_count'],
            'anonymous_sessions': self.privacy_metrics['anonymous_sessions'],
            'security_score': self._calculate_security_score(),
            'last_updated': datetime.utcnow().isoformat()
        }
    
    def _calculate_security_score(self) -> int:
        """Calculate overall security score (0-100)"""
        score = 0
        
        if settings.HIPAA_COMPLIANT:
            score += 25
        if settings.GDPR_COMPLIANT:
            score += 25
        if settings.DATA_ENCRYPTION_ENABLED:
            score += 20
        if settings.LOCAL_PROCESSING_ENABLED:
            score += 15
        if settings.ZERO_KNOWLEDGE_ARCHITECTURE:
            score += 15
        
        return score
    
    def validate_data_retention_policy(self, data_timestamp: datetime) -> bool:
        """Validate data retention policy compliance"""
        retention_period = timedelta(days=7 * 365)  # 7 years for medical data
        return datetime.utcnow() - data_timestamp <= retention_period
    
    def audit_data_access(self, user_id: str, data_type: str, action: str) -> Dict:
        """Audit data access for compliance"""
        audit_log = {
            'timestamp': datetime.utcnow().isoformat(),
            'user_id': hashlib.sha256(user_id.encode()).hexdigest() if settings.ANONYMOUS_MODE_ENABLED else user_id,
            'data_type': data_type,
            'action': action,
            'ip_address': 'anonymized',
            'session_id': secrets.token_urlsafe(16)
        }
        
        # In production, this would be logged to a secure audit system
        print(f"Audit Log: {audit_log}")
        return audit_log

# Singleton instance
privacy_security_service = PrivacySecurityService()
