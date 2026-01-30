"""
CPU Info Parser module for parsing CPU information on Linux and Windows systems.
"""

import platform
import sys
import subprocess
from typing import Dict, Tuple, Optional
from collections import defaultdict


class CpuInfoEntry:
    """Represents a single CPU entry from /proc/cpuinfo."""

    def __init__(self):
        self.is_arm = False
        self.is_x86 = False
        self.implementer: Optional[str] = None
        self.part: Optional[str] = None
        self.vendor_id: Optional[str] = None
        self.model_name: Optional[str] = None
        self.has_info = False

    def reset(self):
        """Reset all fields for a new entry."""
        self.is_arm = False
        self.is_x86 = False
        self.implementer = None
        self.part = None
        self.vendor_id = None
        self.model_name = None
        self.has_info = False

    def parse_line(self, line: str):
        """Parse a single line from cpuinfo and update this entry."""
        line = line.strip()
        if not line:
            return

        self.has_info = True

        try:
            if line.startswith('CPU implementer'):
                self.is_arm = True
                self.is_x86 = False
                implementer = line.split(':')[1].strip().lower()
                # Validate hex format
                if implementer.startswith('0x'):
                    self.implementer = implementer
                else:
                    # Convert decimal to hex
                    try:
                        self.implementer = hex(int(implementer))
                    except ValueError:
                        raise ValueError(f"Invalid CPU implementer value: {implementer}")

            elif line.startswith('CPU part') and self.is_arm:
                part = line.split(':')[1].strip().lower()
                # Validate hex format
                if part.startswith('0x'):
                    self.part = part
                else:
                    # Convert decimal to hex
                    try:
                        self.part = hex(int(part))
                    except ValueError:
                        raise ValueError(f"Invalid CPU part value: {part}")

            elif line.startswith('vendor_id'):
                self.is_x86 = True
                self.is_arm = False
                self.vendor_id = line.split(':')[1].strip()

            elif line.startswith('model name'):
                self.model_name = line.split(':', 1)[1].strip()
        except (IndexError, ValueError) as e:
            raise ValueError(f"Failed to parse cpuinfo line '{line}': {e}")

    def get_key(self) -> Optional[Tuple[str, ...]]:
        """Get a unique key for this CPU entry."""
        if self.is_arm and self.implementer and self.part:
            return (self.implementer, self.part)
        elif self.is_x86 and self.vendor_id and self.model_name:
            return (self.vendor_id, self.model_name)
        return None

    def is_valid(self) -> bool:
        """Check if this entry has valid CPU information."""
        return self.has_info and self.get_key() is not None


class CpuInfoParser:
    """Parser for CPU information on Linux and Windows systems."""

    CPUINFO_PATH = '/proc/cpuinfo'

    def __init__(self):
        self.system = platform.system()

    def parse(self) -> Dict[Tuple[str, ...], int]:
        """
        Parse CPU information and return CPU counts.

        Returns:
            Dictionary mapping CPU keys to counts

        Raises:
            RuntimeError: If parsing fails
        """
        try:
            if self.system == 'Linux':
                return self._parse_linux()
            elif self.system == 'Windows':
                return self._parse_windows()
            else:
                raise RuntimeError(f"Unsupported platform: {self.system}")
        except Exception as e:
            raise RuntimeError(f"Failed to parse CPU information: {e}")

    def _parse_linux(self) -> Dict[Tuple[str, ...], int]:
        """Parse CPU information on Linux systems."""
        try:
            with open(self.CPUINFO_PATH, 'r') as f:
                return self._parse_file(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"{self.CPUINFO_PATH} not found. Is this a Linux system?")

    def _parse_windows(self) -> Dict[Tuple[str, ...], int]:
        """Parse CPU information on Windows systems."""
        cpus_found = defaultdict(int)

        try:
            # Use wmic command to get CPU information
            result = subprocess.run(
                ['wmic', 'cpu', 'get', 'Name,Manufacturer', '/format:list'],
                capture_output=True,
                text=True,
                check=True
            )

            # Parse the output
            lines = result.stdout.strip().split('\n')
            manufacturer = None
            name = None

            for line in lines:
                line = line.strip()
                if not line:
                    continue

                if line.startswith('Manufacturer='):
                    manufacturer = line.split('=', 1)[1].strip()
                elif line.startswith('Name='):
                    name = line.split('=', 1)[1].strip()

            if manufacturer and name:
                # Normalize manufacturer names
                if 'intel' in manufacturer.lower():
                    vendor_id = 'GenuineIntel'
                elif 'amd' in manufacturer.lower():
                    vendor_id = 'AuthenticAMD'
                else:
                    vendor_id = manufacturer

                # Get CPU count
                cpu_count = self._get_windows_cpu_count()
                key = (vendor_id, name)
                cpus_found[key] = cpu_count

        except (subprocess.CalledProcessError, FileNotFoundError):
            # Fallback to platform module if wmic is not available
            return self._parse_windows_fallback()

        return dict(cpus_found)

    def _parse_windows_fallback(self) -> Dict[Tuple[str, ...], int]:
        """Fallback CPU detection for Windows using platform module."""
        cpus_found = defaultdict(int)

        try:
            processor = platform.processor()
            machine = platform.machine()

            if processor:
                # Try to determine vendor from processor name
                processor_lower = processor.lower()
                if 'intel' in processor_lower:
                    vendor_id = 'GenuineIntel'
                elif 'amd' in processor_lower:
                    vendor_id = 'AuthenticAMD'
                else:
                    vendor_id = 'Unknown'

                cpu_count = self._get_windows_cpu_count()
                key = (vendor_id, processor)
                cpus_found[key] = cpu_count
            else:
                raise RuntimeError("Unable to detect CPU information on Windows")

        except Exception as e:
            raise RuntimeError(f"Failed to detect CPU information on Windows: {e}")

        return dict(cpus_found)

    def _get_windows_cpu_count(self) -> int:
        """Get CPU core count on Windows."""
        try:
            # Try using multiprocessing first
            import multiprocessing
            return multiprocessing.cpu_count()
        except ImportError:
            # Fallback to environment variable
            import os
            return int(os.environ.get('NUMBER_OF_PROCESSORS', 1))

    def _parse_file(self, file) -> Dict[Tuple[str, ...], int]:
        """Parse the cpuinfo file content."""
        cpus_found = defaultdict(int)
        current_entry = CpuInfoEntry()

        for line in file:
            line = line.strip()

            if not line:
                # Empty line - finalize current entry
                self._finalize_entry(current_entry, cpus_found)
                current_entry.reset()
                continue

            current_entry.parse_line(line)

        # Handle last entry if file doesn't end with newline
        self._finalize_entry(current_entry, cpus_found)

        return dict(cpus_found)

    def _finalize_entry(self, entry: CpuInfoEntry, cpus_found: Dict[Tuple[str, ...], int]):
        """Finalize a CPU entry and add it to the results."""
        if entry.is_valid():
            key = entry.get_key()
            if key:
                cpus_found[key] += 1