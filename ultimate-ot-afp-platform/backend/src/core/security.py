"""
Security utilities for Ultimate OT-AFP Platform
"""

from datetime import datetime, timedelta
from typing import Any, Union
from jose import jwt, JWTError
from passlib.context import CryptContext
import secrets
import hashlib

from .config import settings


# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT token utilities
def create_access_token(
    subject: Union[str, Any],
    expires_delta: timedelta = None
) -> str:
    """
    Create JWT access token
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def verify_token(token: str) -> Union[str, None]:
    """
    Verify and decode JWT token
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            return None
        return username
    except JWTError:
        return None


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify password against hash
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hash password using bcrypt
    """
    return pwd_context.hash(password)


# API key utilities
def generate_api_key() -> str:
    """
    Generate secure API key
    """
    return secrets.token_urlsafe(32)


def hash_api_key(api_key: str) -> str:
    """
    Hash API key for storage
    """
    return hashlib.sha256(api_key.encode()).hexdigest()


def verify_api_key(api_key: str, hashed_key: str) -> bool:
    """
    Verify API key against stored hash
    """
    return hash_api_key(api_key) == hashed_key


# File security utilities
def calculate_file_hash(file_path: str, algorithm: str = "sha256") -> str:
    """
    Calculate file hash
    """
    hash_obj = hashlib.new(algorithm)
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_obj.update(chunk)
    return hash_obj.hexdigest()


def scan_file_for_malware(file_path: str) -> dict:
    """
    Basic malware scanning (placeholder for integration)
    """
    # This would integrate with actual antivirus engines
    file_hash = calculate_file_hash(file_path)

    # Check against known malware hash databases
    # This is a placeholder implementation
    return {
        "file_path": file_path,
        "hash": file_hash,
        "algorithm": "sha256",
        "malware_detected": False,
        "threat_score": 0.0,
        "scan_results": []
    }


# Network security utilities
def validate_ip_address(ip: str) -> bool:
    """
    Validate IP address format
    """
    import ipaddress
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename to prevent path traversal
    """
    import re
    import os

    # Remove path separators and dangerous characters
    sanitized = re.sub(r'[<>:"/\\|?*]', '', filename)
    sanitized = sanitized.strip()

    # Ensure filename is not too long
    if len(sanitized) > 255:
        name, ext = os.path.splitext(sanitized)
        sanitized = name[:255-len(ext)] + ext

    return sanitized


# Encryption utilities
def generate_encryption_key() -> bytes:
    """
    Generate encryption key for data protection
    """
    return secrets.token_bytes(32)


def encrypt_data(data: str, key: bytes) -> str:
    """
    Encrypt sensitive data
    """
    from cryptography.fernet import Fernet
    f = Fernet(key)
    return f.encrypt(data.encode()).decode()


def decrypt_data(encrypted_data: str, key: bytes) -> str:
    """
    Decrypt sensitive data
    """
    from cryptography.fernet import Fernet
    f = Fernet(key)
    return f.decrypt(encrypted_data.encode()).decode()


# Audit logging
def log_security_event(event_type: str, details: dict, user: str = None):
    """
    Log security-related events
    """
    import structlog
    logger = structlog.get_logger("security")

    log_entry = {
        "event_type": event_type,
        "timestamp": datetime.utcnow().isoformat(),
        "user": user,
        "details": details
    }

    logger.warning("Security event", **log_entry)