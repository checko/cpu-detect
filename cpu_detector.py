"""
CPU Detector module for identifying CPU architecture and family.
"""

from typing import Dict, Tuple, List, NamedTuple
from cpu_database import ArmCpuDatabase, X86CpuDatabase
from cpuinfo_parser import CpuInfoParser


class CpuInfo(NamedTuple):
    """Information about a detected CPU."""
    core_count: int
    vendor_implementer: str
    model_part: str
    model_name: str
    architecture: str


class CpuDetector:
    """Main CPU detection orchestrator."""

    def __init__(self):
        self.arm_db = ArmCpuDatabase()
        self.x86_db = X86CpuDatabase()
        self.parser = CpuInfoParser()

    def detect_cpus(self) -> List[CpuInfo]:
        """
        Detect and identify all CPUs on the system.

        Returns:
            List of CpuInfo objects for each detected CPU type

        Raises:
            RuntimeError: If no CPUs are detected or parsing fails
        """
        try:
            raw_cpus = self.parser.parse()
        except Exception as e:
            raise RuntimeError(f"Failed to parse CPU information: {e}") from e

        if not raw_cpus:
            raise RuntimeError("No CPU information found in /proc/cpuinfo")

        detected_cpus = []

        for key, count in raw_cpus.items():
            if len(key) != 2:
                continue  # Skip invalid keys

            try:
                cpu_info = self._identify_cpu(key, count)
                detected_cpus.append(cpu_info)
            except Exception as e:
                # Log the error but continue processing other CPUs
                print(f"Warning: Failed to identify CPU with key {key}: {e}", file=sys.stderr)
                continue

        if not detected_cpus:
            raise RuntimeError("Failed to identify any CPUs from the parsed data")

        return detected_cpus

    def _identify_cpu(self, key: Tuple[str, ...], count: int) -> CpuInfo:
        """
        Identify a CPU based on its key and count.

        Args:
            key: CPU key tuple (implementer/part or vendor/model)
            count: Number of cores

        Returns:
            CpuInfo object with identified CPU details
        """
        implementer_or_vendor, part_or_model = key

        # Check if this is an ARM CPU (part starts with 0x and is 4 chars)
        if (isinstance(part_or_model, str) and
            part_or_model.startswith('0x') and
            len(part_or_model) == 4):

            return self._identify_arm_cpu(implementer_or_vendor, part_or_model, count)
        else:
            return self._identify_x86_cpu(implementer_or_vendor, part_or_model, count)

    def _identify_arm_cpu(self, implementer: str, part: str, count: int) -> CpuInfo:
        """Identify an ARM CPU."""
        cpu_info = self.arm_db.get_cpu_info(implementer, part)

        if cpu_info:
            model_name, architecture = cpu_info
        else:
            model_name = "Unknown"
            architecture = "Unknown (AArch64)"

        return CpuInfo(
            core_count=count,
            vendor_implementer=implementer,
            model_part=part,
            model_name=model_name,
            architecture=architecture
        )

    def _identify_x86_cpu(self, vendor_id: str, model_name: str, count: int) -> CpuInfo:
        """Identify an x86 CPU."""
        architecture = self.x86_db.get_architecture(vendor_id)
        matched_model = self.x86_db.find_matching_model(vendor_id, model_name)

        display_model = matched_model if matched_model else "Unknown"

        return CpuInfo(
            core_count=count,
            vendor_implementer=vendor_id,
            model_part=model_name,
            model_name=display_model,
            architecture=architecture
        )