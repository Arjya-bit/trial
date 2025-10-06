"""
FTK Emulator Module
Emulates Forensic Toolkit (FTK) functionality
"""

from .disk_imaging import DiskImager
from .file_carving import FileCarver

__all__ = [
    "DiskImager",
    "FileCarver"
]