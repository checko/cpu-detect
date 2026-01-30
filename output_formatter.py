"""
Output formatting module for displaying CPU detection results.
"""

from typing import List
from cpu_detector import CpuInfo


class CpuOutputFormatter:
    """Formatter for CPU detection output."""

    def __init__(self):
        self.column_widths = {
            'core_count': 12,
            'vendor': 20,
            'model': 30,
            'architecture': 15
        }

    def print_results(self, cpus: List[CpuInfo]):
        """
        Print CPU detection results in a formatted table.

        Args:
            cpus: List of CpuInfo objects to display
        """
        if not cpus:
            print("No CPUs detected.")
            return

        self._print_header()
        self._print_separator()
        self._print_cpu_rows(cpus)

    def _print_header(self):
        """Print the table header."""
        header = ("{:<{core_count}} {:<{vendor}} {:<{model}} {:<{arch}}".format(
            'Core Count',
            'Vendor/Implementer',
            'Model',
            'Architecture',
            core_count=self.column_widths['core_count'],
            vendor=self.column_widths['vendor'],
            model=self.column_widths['model'],
            arch=self.column_widths['architecture']
        ))
        print(header)

    def _print_separator(self):
        """Print the table separator line."""
        total_width = sum(self.column_widths.values()) + 3  # +3 for spaces between columns
        print("-" * total_width)

    def _print_cpu_rows(self, cpus: List[CpuInfo]):
        """Print the CPU information rows."""
        for cpu in cpus:
            # For ARM CPUs, show implementer and part
            if cpu.model_part.startswith('0x'):
                vendor_display = cpu.vendor_implementer
                model_display = f"{cpu.model_part:<10} {cpu.model_name}"
            else:
                # For x86 CPUs, show vendor and model name
                vendor_display = cpu.vendor_implementer
                model_display = cpu.model_part

            row = ("{:<{core_count}} {:<{vendor}} {:<{model}} {:<{arch}}".format(
                cpu.core_count,
                vendor_display,
                model_display,
                cpu.architecture,
                core_count=self.column_widths['core_count'],
                vendor=self.column_widths['vendor'],
                model=self.column_widths['model'],
                arch=self.column_widths['architecture']
            ))
            print(row)