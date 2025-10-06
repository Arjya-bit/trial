"""
Core module for Ultimate OT-AFP Platform
"""

from .app import create_application
from .config import settings
from .database import get_db, init_database, check_database_health
from .security import (
    create_access_token,
    verify_token,
    verify_password,
    get_password_hash,
    generate_api_key,
    hash_api_key,
    verify_api_key,
    calculate_file_hash,
    scan_file_for_malware,
    validate_ip_address,
    sanitize_filename,
    generate_encryption_key,
    encrypt_data,
    decrypt_data,
    log_security_event
)

__all__ = [
    "create_application",
    "settings",
    "get_db",
    "init_database",
    "check_database_health",
    "create_access_token",
    "verify_token",
    "verify_password",
    "get_password_hash",
    "generate_api_key",
    "hash_api_key",
    "verify_api_key",
    "calculate_file_hash",
    "scan_file_for_malware",
    "validate_ip_address",
    "sanitize_filename",
    "generate_encryption_key",
    "encrypt_data",
    "decrypt_data",
    "log_security_event"
]