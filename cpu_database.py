"""
CPU Database module containing information about various CPU architectures and models.
"""

from typing import Dict, List, Tuple, Optional


class ArmCpuDatabase:
    """Database for ARM CPU information."""

    def __init__(self):
        self._db: Dict[str, Dict[str, Tuple[str, str]]] = {
            '0x41': {  # ARM Limited
                '0xd03': ('Cortex-A53', 'ARMv8.0-A'),
                '0xd04': ('Cortex-A35', 'ARMv8.0-A'),
                '0xd05': ('Cortex-A55', 'ARMv8.2-A'),
                '0xd06': ('Cortex-A65', 'ARMv8.2-A'),
                '0xd07': ('Cortex-A57', 'ARMv8.0-A'),
                '0xd08': ('Cortex-A72', 'ARMv8.0-A'),
                '0xd09': ('Cortex-A73', 'ARMv8.0-A'),
                '0xd0a': ('Cortex-A75', 'ARMv8.2-A'),
                '0xd0b': ('Cortex-A76', 'ARMv8.2-A'),
                '0xd0c': ('Neoverse N1', 'ARMv8.2-A'),
                '0xd0d': ('Cortex-A77', 'ARMv8.2-A'),
                '0xd40': ('Neoverse V1', 'ARMv8.4-A'),
                '0xd41': ('Cortex-A78', 'ARMv8.2-A'),
                '0xd44': ('Cortex-X1', 'ARMv8.2-A'),
                '0xd46': ('Cortex-A510', 'ARMv9.0-A'),
                '0xd47': ('Cortex-A710', 'ARMv9.0-A'),
                '0xd48': ('Cortex-X2', 'ARMv9.0-A'),
                '0xd49': ('Neoverse N2', 'ARMv9.0-A'),
                '0xd4a': ('Neoverse E1', 'ARMv8.2-A'),
                '0xd4b': ('Cortex-A78C', 'ARMv8.2-A'),
                '0xd4c': ('Cortex-X3', 'ARMv9.0-A'),
                '0xd4d': ('Cortex-A715', 'ARMv9.0-A'),
                '0xd4e': ('Cortex-X4', 'ARMv9.2-A'),
                '0xd80': ('Cortex-A520', 'ARMv9.2-A'),
                '0xd81': ('Cortex-A720', 'ARMv9.2-A'),
                '0xd82': ('Cortex-X4', 'ARMv9.2-A'),
                '0xd84': ('Cortex-A525', 'ARMv9.2-A'),
                '0xd85': ('Cortex-X925', 'ARMv9.2-A'),
                '0xd87': ('Cortex-A725', 'ARMv9.2-A'),
            },
            # Apple, Qualcomm, Samsung, etc. have their own IDs,
            # but Linux typically reports 0x41 (ARM) for reference designs.
        }

    def get_cpu_info(self, implementer: str, part: str) -> Optional[Tuple[str, str]]:
        """
        Get CPU model name and architecture for given implementer and part.

        Args:
            implementer: CPU implementer ID (hex string)
            part: CPU part ID (hex string)

        Returns:
            Tuple of (model_name, architecture) or None if not found
        """
        implementer_db = self._db.get(implementer.lower())
        if implementer_db:
            return implementer_db.get(part.lower())
        return None


class X86CpuDatabase:
    """Database for x86 CPU information."""

    def __init__(self):
        self._db: Dict[str, List[Tuple[str, str]]] = {
            'GenuineIntel': [
                ('Intel Core i3', 'x86_64'),
                ('Intel Core i5', 'x86_64'),
                ('Intel Core i7', 'x86_64'),
                ('Intel Core i9', 'x86_64'),
                ('Intel Xeon', 'x86_64'),
                ('Intel Atom', 'x86_64'),
                ('Intel Celeron', 'x86_64'),
            ],
            'AuthenticAMD': [
                ('AMD Ryzen', 'x86_64'),
                ('AMD Phenom', 'x86_64'),
                ('AMD Athlon', 'x86_64'),
                ('AMD EPYC', 'x86_64'),
                ('AMD A-Series', 'x86_64'),
            ],
        }

    def get_architecture(self, vendor_id: str) -> str:
        """
        Get architecture for a vendor.

        Args:
            vendor_id: CPU vendor ID

        Returns:
            Architecture string (default: x86_64)
        """
        # All current x86 CPUs in our database are x86_64
        return 'x86_64'

    def find_matching_model(self, vendor_id: str, model_name: str) -> Optional[str]:
        """
        Find a matching model name from the database.

        Args:
            vendor_id: CPU vendor ID
            model_name: Full model name from cpuinfo

        Returns:
            Matching model prefix or None
        """
        if vendor_id not in self._db:
            return None

        model_name_lower = model_name.lower()
        for prefix, _ in self._db[vendor_id]:
            if prefix.lower() in model_name_lower:
                return prefix

        return None