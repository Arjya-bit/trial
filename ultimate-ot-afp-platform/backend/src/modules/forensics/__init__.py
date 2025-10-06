"""
Forensics Module for Ultimate OT-AFP Platform
Provides comprehensive digital forensics capabilities
"""

from .autopsy_emulator import AutopsyEmulator
from .belkasoft_emulator import BelkasoftEmulator
from .ftk_emulator import FTKEmulator
from .oxygen_emulator import OxygenEmulator
from .advanced_forensics import AdvancedForensics

__all__ = [
    "AutopsyEmulator",
    "BelkasoftEmulator",
    "FTKEmulator",
    "OxygenEmulator",
    "AdvancedForensics"
]