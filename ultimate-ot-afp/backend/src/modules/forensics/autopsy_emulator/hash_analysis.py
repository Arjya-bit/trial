"""
Autopsy Digital Forensics Emulator
"""

import hashlib
import logging
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
import asyncio
import json
from dataclasses import dataclass
import time

logger = logging.getLogger(__name__)

@dataclass
class HashResult:
    """Hash analysis result"""
    file_path: str
    md5: str
    sha1: str
    sha256: str
    file_size: int
    known_good: bool
    known_bad: bool
    reputation_score: float

@dataclass
class KeywordSearchResult:
    """Keyword search result"""
    keyword: str
    file_path: str
    line_number: int
    context: str
    match_count: int

class AutopsyEmulator:
    """Autopsy Digital Forensics Platform Emulator"""
    
    def __init__(self):
        self.known_good_hashes = set()
        self.known_bad_hashes = set()
        self.case_directory = Path("./cases")
        self.evidence_directory = Path("./evidence")
        self.case_directory.mkdir(exist_ok=True)
        self.evidence_directory.mkdir(exist_ok=True)
        logger.info("🔍 Autopsy Emulator initialized")
    
    async def create_case(self, case_name: str, examiner: str, description: str = "") -> Dict[str, Any]:
        """Create a new forensics case"""
        try:
            case_id = f"case_{int(time.time())}"
            case_path = self.case_directory / case_id
            case_path.mkdir(exist_ok=True)
            
            case_info = {
                "case_id": case_id,
                "case_name": case_name,
                "examiner": examiner,
                "description": description,
                "created_at": time.time(),
                "case_path": str(case_path),
                "data_sources": [],
                "analysis_results": {}
            }
            
            # Save case metadata
            case_file = case_path / "case_info.json"
            with open(case_file, 'w') as f:
                json.dump(case_info, f, indent=2)
            
            logger.info(f"📁 Created forensics case: {case_name} ({case_id})")
            return case_info
            
        except Exception as e:
            logger.error(f"❌ Failed to create case: {e}")
            raise
    
    async def add_data_source(self, case_id: str, source_path: str, source_type: str = "disk_image") -> bool:
        """Add data source to forensics case"""
        try:
            case_path = self.case_directory / case_id
            case_file = case_path / "case_info.json"
            
            if not case_file.exists():
                raise ValueError(f"Case {case_id} not found")
            
            with open(case_file, 'r') as f:
                case_info = json.load(f)
            
            data_source = {
                "source_id": f"ds_{len(case_info['data_sources'])}",
                "source_path": source_path,
                "source_type": source_type,
                "added_at": time.time(),
                "processed": False
            }
            
            case_info['data_sources'].append(data_source)
            
            with open(case_file, 'w') as f:
                json.dump(case_info, f, indent=2)
            
            logger.info(f"📂 Added data source to case {case_id}: {source_path}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to add data source: {e}")
            return False
    
    async def hash_analysis(self, file_path: str) -> HashResult:
        """Perform comprehensive hash analysis"""
        try:
            path = Path(file_path)
            if not path.exists():
                raise FileNotFoundError(f"File not found: {file_path}")
            
            # Calculate hashes
            md5_hash = hashlib.md5()
            sha1_hash = hashlib.sha1()
            sha256_hash = hashlib.sha256()
            
            with open(path, 'rb') as f:
                while chunk := f.read(8192):
                    md5_hash.update(chunk)
                    sha1_hash.update(chunk)
                    sha256_hash.update(chunk)
            
            md5_result = md5_hash.hexdigest()
            sha1_result = sha1_hash.hexdigest()
            sha256_result = sha256_hash.hexdigest()
            
            # Check against known good/bad databases
            known_good = sha256_result in self.known_good_hashes
            known_bad = sha256_result in self.known_bad_hashes
            
            # Calculate reputation score
            reputation_score = self._calculate_reputation_score(md5_result, sha1_result, sha256_result)
            
            result = HashResult(
                file_path=str(path),
                md5=md5_result,
                sha1=sha1_result,
                sha256=sha256_result,
                file_size=path.stat().st_size,
                known_good=known_good,
                known_bad=known_bad,
                reputation_score=reputation_score
            )
            
            logger.info(f"🔑 Hash analysis completed for: {path.name}")
            return result
            
        except Exception as e:
            logger.error(f"❌ Hash analysis failed: {e}")
            raise
    
    async def keyword_search(self, search_path: str, keywords: List[str], 
                           case_insensitive: bool = True) -> List[KeywordSearchResult]:
        """Perform keyword search across files"""
        try:
            results = []
            search_path = Path(search_path)
            
            if search_path.is_file():
                files_to_search = [search_path]
            else:
                files_to_search = list(search_path.rglob("*"))
                files_to_search = [f for f in files_to_search if f.is_file()]
            
            for file_path in files_to_search:
                try:
                    # Skip binary files
                    if self._is_binary_file(file_path):
                        continue
                    
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = f.readlines()
                    
                    for line_num, line in enumerate(lines, 1):
                        line_content = line if not case_insensitive else line.lower()
                        
                        for keyword in keywords:
                            search_keyword = keyword if not case_insensitive else keyword.lower()
                            
                            if search_keyword in line_content:
                                context_start = max(0, line_num - 2)
                                context_end = min(len(lines), line_num + 2)
                                context = ''.join(lines[context_start:context_end])
                                
                                result = KeywordSearchResult(
                                    keyword=keyword,
                                    file_path=str(file_path),
                                    line_number=line_num,
                                    context=context.strip(),
                                    match_count=line_content.count(search_keyword)
                                )
                                results.append(result)
                
                except Exception as e:
                    logger.warning(f"⚠️ Could not search file {file_path}: {e}")
                    continue
            
            logger.info(f"🔍 Keyword search completed. Found {len(results)} matches")
            return results
            
        except Exception as e:
            logger.error(f"❌ Keyword search failed: {e}")
            return []
    
    async def file_recovery(self, disk_path: str, output_dir: str) -> Dict[str, Any]:
        """Recover deleted files from disk image"""
        try:
            logger.info(f"🔄 Starting file recovery from: {disk_path}")
            
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
            
            # Simulate file recovery process
            recovered_files = []
            
            # In a real implementation, this would use tools like:
            # - sleuthkit (TSK)
            # - photorec
            # - foremost
            
            # For demonstration, create some mock recovered files
            recovery_results = {
                "disk_path": disk_path,
                "output_directory": str(output_path),
                "recovered_files": recovered_files,
                "recovery_time": time.time(),
                "status": "completed",
                "files_recovered": len(recovered_files),
                "total_size": 0
            }
            
            logger.info(f"✅ File recovery completed. Recovered {len(recovered_files)} files")
            return recovery_results
            
        except Exception as e:
            logger.error(f"❌ File recovery failed: {e}")
            return {"status": "failed", "error": str(e)}
    
    async def timeline_analysis(self, case_id: str, start_time: float = None, 
                              end_time: float = None) -> List[Dict[str, Any]]:
        """Generate timeline analysis"""
        try:
            logger.info(f"📅 Generating timeline analysis for case: {case_id}")
            
            case_path = self.case_directory / case_id
            timeline_events = []
            
            # Analyze file system events
            for data_source_path in case_path.glob("**/*"):
                if data_source_path.is_file():
                    stat = data_source_path.stat()
                    
                    # File creation event
                    if not start_time or stat.st_ctime >= start_time:
                        if not end_time or stat.st_ctime <= end_time:
                            timeline_events.append({
                                "timestamp": stat.st_ctime,
                                "event_type": "file_created",
                                "file_path": str(data_source_path),
                                "file_size": stat.st_size,
                                "description": f"File created: {data_source_path.name}"
                            })
                    
                    # File modification event
                    if not start_time or stat.st_mtime >= start_time:
                        if not end_time or stat.st_mtime <= end_time:
                            timeline_events.append({
                                "timestamp": stat.st_mtime,
                                "event_type": "file_modified",
                                "file_path": str(data_source_path),
                                "file_size": stat.st_size,
                                "description": f"File modified: {data_source_path.name}"
                            })
            
            # Sort by timestamp
            timeline_events.sort(key=lambda x: x['timestamp'])
            
            logger.info(f"📊 Timeline analysis completed. Found {len(timeline_events)} events")
            return timeline_events
            
        except Exception as e:
            logger.error(f"❌ Timeline analysis failed: {e}")
            return []
    
    async def generate_report(self, case_id: str, report_format: str = "json") -> Dict[str, Any]:
        """Generate comprehensive forensics report"""
        try:
            logger.info(f"📋 Generating report for case: {case_id}")
            
            case_path = self.case_directory / case_id
            case_file = case_path / "case_info.json"
            
            if not case_file.exists():
                raise ValueError(f"Case {case_id} not found")
            
            with open(case_file, 'r') as f:
                case_info = json.load(f)
            
            # Generate comprehensive report
            report = {
                "case_info": case_info,
                "generated_at": time.time(),
                "report_format": report_format,
                "examiner_notes": [],
                "evidence_summary": {
                    "total_files_analyzed": 0,
                    "suspicious_files": 0,
                    "hash_matches": 0,
                    "keywords_found": 0
                },
                "recommendations": [
                    "Review all flagged suspicious files",
                    "Verify hash matches against external databases",
                    "Conduct additional keyword searches if needed",
                    "Document chain of custody for all evidence"
                ]
            }
            
            # Save report
            report_file = case_path / f"forensics_report.{report_format}"
            if report_format == "json":
                with open(report_file, 'w') as f:
                    json.dump(report, f, indent=2)
            
            logger.info(f"✅ Forensics report generated: {report_file}")
            return report
            
        except Exception as e:
            logger.error(f"❌ Report generation failed: {e}")
            raise
    
    def _calculate_reputation_score(self, md5: str, sha1: str, sha256: str) -> float:
        """Calculate file reputation score"""
        score = 0.5  # Neutral baseline
        
        if sha256 in self.known_good_hashes:
            score += 0.4
        elif sha256 in self.known_bad_hashes:
            score -= 0.4
        
        # Additional reputation factors could be added here
        
        return max(0.0, min(1.0, score))
    
    def _is_binary_file(self, file_path: Path) -> bool:
        """Check if file is binary"""
        try:
            with open(file_path, 'rb') as f:
                chunk = f.read(1024)
                return b'\0' in chunk
        except:
            return True
    
    async def load_hash_databases(self, good_hashes_file: str = None, 
                                bad_hashes_file: str = None):
        """Load known good/bad hash databases"""
        try:
            if good_hashes_file and Path(good_hashes_file).exists():
                with open(good_hashes_file, 'r') as f:
                    self.known_good_hashes = set(line.strip() for line in f)
                logger.info(f"📥 Loaded {len(self.known_good_hashes)} known good hashes")
            
            if bad_hashes_file and Path(bad_hashes_file).exists():
                with open(bad_hashes_file, 'r') as f:
                    self.known_bad_hashes = set(line.strip() for line in f)
                logger.info(f"📥 Loaded {len(self.known_bad_hashes)} known bad hashes")
                
        except Exception as e:
            logger.error(f"❌ Failed to load hash databases: {e}")

# Global Autopsy emulator instance
autopsy_emulator = AutopsyEmulator()