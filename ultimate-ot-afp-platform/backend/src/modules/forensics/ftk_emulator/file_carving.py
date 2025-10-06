"""
FTK File Carving Module
Emulates FTK file carving capabilities for data recovery
"""

import os
import logging
import asyncio
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import re

logger = logging.getLogger(__name__)


class FileCarver:
    """Emulates FTK file carving functionality"""

    def __init__(self):
        # File signatures for carving
        self.file_signatures = {
            # Images
            ".jpg": [b"\xFF\xD8\xFF"],
            ".jpeg": [b"\xFF\xD8\xFF"],
            ".png": [b"\x89PNG"],
            ".gif": [b"GIF87a", b"GIF89a"],
            ".bmp": [b"BM"],
            ".tiff": [b"II*\x00", b"MM\x00*"],
            ".webp": [b"RIFF", b"WEBP"],

            # Documents
            ".pdf": [b"%PDF-"],
            ".doc": [b"\xD0\xCF\x11\xE0\xA1\xB1\x1A\xE1"],
            ".docx": [b"PK\x03\x04"],
            ".xls": [b"\xD0\xCF\x11\xE0\xA1\xB1\x1A\xE1"],
            ".xlsx": [b"PK\x03\x04"],
            ".ppt": [b"\xD0\xCF\x11\xE0\xA1\xB1\x1A\xE1"],
            ".pptx": [b"PK\x03\x04"],
            ".txt": [b""],  # Text files don't have reliable signatures

            # Archives
            ".zip": [b"PK\x03\x04", b"PK\x05\x06", b"PK\x07\x08"],
            ".rar": [b"Rar!\x1A\x07"],
            ".7z": [b"7z\xBC\xAF\x27\x1C"],
            ".tar": [b"ustar\x00", b"ustar\x2000"],
            ".gz": [b"\x1F\x8B"],

            # Executables
            ".exe": [b"MZ"],
            ".dll": [b"MZ"],
            ".elf": [b"\x7FELF"],
            ".pe": [b"MZ"],

            # Videos
            ".mp4": [b"\x00\x00\x00\x20ftyp"],
            ".avi": [b"RIFF", b"AVI "],
            ".mkv": [b"\x1A\x45\xDF\xA3"],
            ".mov": [b"\x00\x00\x00\x14ftyp"],

            # Audio
            ".mp3": [b"\xFF\xFB", b"\xFF\xF3", b"\xFF\xF2"],
            ".wav": [b"RIFF", b"WAVE"],
            ".flac": [b"fLaC"],
        }

        # Maximum file size to carve (to prevent memory issues)
        self.max_file_size = 100 * 1024 * 1024  # 100MB

    async def carve_files(
        self,
        image_path: str,
        output_dir: str,
        file_types: Optional[List[str]] = None,
        max_files: int = 1000
    ) -> Dict:
        """
        Carve files from disk image

        Args:
            image_path: Path to disk image file
            output_dir: Directory to save carved files
            file_types: List of file extensions to search for (None for all)
            max_files: Maximum number of files to carve

        Returns:
            Dict with carving results
        """
        try:
            logger.info(f"Starting file carving: {image_path}")

            if not os.path.exists(image_path):
                return {"error": f"Image file does not exist: {image_path}"}

            # Create output directory
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)

            # Filter file types if specified
            signatures_to_use = self.file_signatures
            if file_types:
                signatures_to_use = {
                    ext: sigs for ext, sigs in self.file_signatures.items()
                    if ext in file_types
                }

            carved_files = []
            files_found = 0

            # Read image file in chunks
            with open(image_path, 'rb') as image_file:
                offset = 0
                chunk_size = 8192

                while offset < os.path.getsize(image_path) and files_found < max_files:
                    chunk = image_file.read(chunk_size)
                    if not chunk:
                        break

                    # Search for file signatures in chunk
                    for ext, signatures in signatures_to_use.items():
                        for signature in signatures:
                            sig_positions = self._find_signature(chunk, signature)
                            for pos in sig_positions:
                                absolute_offset = offset + pos

                                # Try to carve file starting at this position
                                carved_file = await self._carve_single_file(
                                    image_file, absolute_offset, ext, output_path
                                )

                                if carved_file:
                                    carved_files.append(carved_file)
                                    files_found += 1

                                    if files_found >= max_files:
                                        break

                            if files_found >= max_files:
                                break

                        if files_found >= max_files:
                            break

                    offset += chunk_size

            return {
                "success": True,
                "image_path": image_path,
                "output_dir": str(output_path),
                "files_carved": len(carved_files),
                "carved_files": carved_files,
                "max_files_reached": files_found >= max_files
            }

        except Exception as e:
            logger.error(f"Error during file carving: {e}")
            return {"error": str(e)}

    def _find_signature(self, data: bytes, signature: bytes) -> List[int]:
        """Find all occurrences of signature in data"""
        positions = []
        offset = 0

        while True:
            pos = data.find(signature, offset)
            if pos == -1:
                break
            positions.append(pos)
            offset = pos + 1

        return positions

    async def _carve_single_file(
        self,
        image_file: asyncio.Handle,
        offset: int,
        file_ext: str,
        output_dir: Path
    ) -> Optional[Dict]:
        """Carve a single file from the image"""
        try:
            # Save current position
            current_pos = image_file.tell()

            # Seek to file start
            image_file.seek(offset)

            # For different file types, use different carving strategies
            if file_ext in [".jpg", ".jpeg", ".png", ".gif", ".bmp"]:
                return await self._carve_by_delimiter(image_file, file_ext, output_dir, b'\xFF\xD9')
            elif file_ext in [".pdf"]:
                return await self._carve_by_delimiter(image_file, file_ext, output_dir, b"%%EOF")
            elif file_ext in [".zip", ".docx", ".xlsx"]:
                return await self._carve_by_size(image_file, file_ext, output_dir, 1024*1024)  # 1MB max
            elif file_ext in [".txt"]:
                return await self._carve_text_file(image_file, file_ext, output_dir)
            else:
                # Default: try to carve by reading until end of meaningful data
                return await self._carve_by_heuristic(image_file, file_ext, output_dir)

        except Exception as e:
            logger.error(f"Error carving file at offset {offset}: {e}")
            return None
        finally:
            # Restore file position
            image_file.seek(current_pos)

    async def _carve_by_delimiter(
        self,
        image_file: asyncio.Handle,
        file_ext: str,
        output_dir: Path,
        delimiter: bytes
    ) -> Optional[Dict]:
        """Carve file by reading until delimiter"""
        try:
            file_data = bytearray()
            chunk_size = 8192

            # Read until we find the delimiter or reach max size
            while len(file_data) < self.max_file_size:
                chunk = image_file.read(chunk_size)
                if not chunk:
                    break

                file_data.extend(chunk)

                # Check if delimiter is in the chunk we just read
                if delimiter in chunk:
                    # Remove everything after the delimiter
                    delimiter_pos = file_data.rfind(delimiter)
                    if delimiter_pos >= 0:
                        file_data = file_data[:delimiter_pos + len(delimiter)]
                    break

            if len(file_data) > 0:
                # Generate filename
                filename = f"carved_{int(time.time())}_{len(file_data)}{file_ext}"
                output_path = output_dir / filename

                # Write file
                with open(output_path, 'wb') as f:
                    f.write(file_data)

                return {
                    "filename": filename,
                    "path": str(output_path),
                    "size": len(file_data),
                    "offset": offset,
                    "file_type": file_ext
                }

        except Exception as e:
            logger.error(f"Error carving by delimiter: {e}")

        return None

    async def _carve_by_size(
        self,
        image_file: asyncio.Handle,
        file_ext: str,
        output_dir: Path,
        max_size: int
    ) -> Optional[Dict]:
        """Carve file by reading fixed size"""
        try:
            file_data = image_file.read(max_size)
            if len(file_data) == 0:
                return None

            filename = f"carved_{int(time.time())}_{len(file_data)}{file_ext}"
            output_path = output_dir / filename

            with open(output_path, 'wb') as f:
                f.write(file_data)

            return {
                "filename": filename,
                "path": str(output_path),
                "size": len(file_data),
                "offset": offset,
                "file_type": file_ext
            }

        except Exception as e:
            logger.error(f"Error carving by size: {e}")

        return None

    async def _carve_text_file(
        self,
        image_file: asyncio.Handle,
        file_ext: str,
        output_dir: Path
    ) -> Optional[Dict]:
        """Carve text file by reading until non-printable characters"""
        try:
            file_data = bytearray()
            chunk_size = 8192

            # Read text data (printable ASCII characters)
            while len(file_data) < self.max_file_size:
                chunk = image_file.read(chunk_size)
                if not chunk:
                    break

                # Keep only printable ASCII characters
                text_chunk = bytes(c for c in chunk if 32 <= c <= 126 or c in [9, 10, 13])
                file_data.extend(text_chunk)

                # Stop if we encounter too many non-printable characters
                if len(text_chunk) < len(chunk) * 0.5:  # Less than 50% printable
                    break

            if len(file_data) > 100:  # Minimum size for text file
                filename = f"carved_{int(time.time())}_{len(file_data)}{file_ext}"
                output_path = output_dir / filename

                with open(output_path, 'wb') as f:
                    f.write(file_data)

                return {
                    "filename": filename,
                    "path": str(output_path),
                    "size": len(file_data),
                    "offset": offset,
                    "file_type": file_ext
                }

        except Exception as e:
            logger.error(f"Error carving text file: {e}")

        return None

    async def _carve_by_heuristic(
        self,
        image_file: asyncio.Handle,
        file_ext: str,
        output_dir: Path
    ) -> Optional[Dict]:
        """Carve file using heuristic approach"""
        # For now, use size-based carving as fallback
        return await self._carve_by_size(image_file, file_ext, output_dir, 1024*1024)

    async def get_file_signatures(self) -> Dict:
        """Get all supported file signatures"""
        return self.file_signatures.copy()

    async def add_file_signature(self, extension: str, signatures: List[bytes]):
        """Add new file signature"""
        if extension not in self.file_signatures:
            self.file_signatures[extension] = []

        self.file_signatures[extension].extend(signatures)
        logger.info(f"Added signatures for {extension}")

    async def search_for_files(self, image_path: str, file_types: Optional[List[str]] = None) -> Dict:
        """
        Search for files in disk image without carving

        Args:
            image_path: Path to disk image
            file_types: List of file extensions to search for

        Returns:
            Dict with search results
        """
        try:
            if not os.path.exists(image_path):
                return {"error": f"Image file does not exist: {image_path}"}

            # Filter signatures
            signatures_to_use = self.file_signatures
            if file_types:
                signatures_to_use = {
                    ext: sigs for ext, sigs in self.file_signatures.items()
                    if ext in file_types
                }

            found_files = {}

            with open(image_path, 'rb') as image_file:
                offset = 0
                chunk_size = 8192

                while offset < os.path.getsize(image_path):
                    chunk = image_file.read(chunk_size)
                    if not chunk:
                        break

                    # Search for signatures
                    for ext, signatures in signatures_to_use.items():
                        for signature in signatures:
                            positions = self._find_signature(chunk, signature)
                            for pos in positions:
                                absolute_offset = offset + pos
                                if ext not in found_files:
                                    found_files[ext] = []

                                found_files[ext].append({
                                    "offset": absolute_offset,
                                    "signature": signature.hex()
                                })

                    offset += chunk_size

            return {
                "success": True,
                "image_path": image_path,
                "found_files": found_files,
                "total_signatures_found": sum(len(files) for files in found_files.values())
            }

        except Exception as e:
            return {"error": str(e)}