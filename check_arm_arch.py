#!/usr/bin/env python3
"""
CPU Architecture Detection Tool

This tool identifies the host CPU architecture and family by parsing
/proc/cpuinfo on Linux systems. It supports both ARM and x86 architectures.
"""

import sys
from cpu_detector import CpuDetector
from output_formatter import CpuOutputFormatter


def main():
    """Main entry point for CPU detection."""
    try:
        detector = CpuDetector()
        formatter = CpuOutputFormatter()

        cpus = detector.detect_cpus()
        formatter.print_results(cpus)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()