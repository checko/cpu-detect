#!/usr/bin/env python3
import sys
import platform

def get_cpu_architecture():
    # ARM CPU database: Implementer -> Part -> (Model Name, Architecture)
    # 0x41 is ARM Limited
    arm_cpu_db = {
        '0x41': {
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

    # x86 CPU database: Vendor -> Model Name
    x86_cpu_db = {
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

    cpus_found = {}

    # Try to detect platform first
    system = platform.system()
    if system != 'Linux':
        print(f"Error: This script is designed for Linux systems.")
        print(f"Current platform: {system}")
        sys.exit(1)

    try:
        with open('/proc/cpuinfo', 'r') as f:
            is_arm = False
            is_x86 = False
            implementer = None
            part = None
            vendor_id = None
            model_name = None

            for line in f:
                line = line.strip()
                if not line:
                    # End of a processor block
                    if implementer and part:
                        key = (implementer, part)
                        if key not in cpus_found:
                            cpus_found[key] = 0
                        cpus_found[key] += 1
                    elif vendor_id and model_name:
                        key = (vendor_id, model_name)
                        if key not in cpus_found:
                            cpus_found[key] = 0
                        cpus_found[key] += 1
                    is_arm = False
                    is_x86 = False
                    implementer = None
                    part = None
                    vendor_id = None
                    model_name = None
                    continue

                if line.startswith('CPU implementer'):
                    is_arm = True
                    is_x86 = False
                    implementer = line.split(':')[1].strip().lower()
                    if not implementer.startswith('0x'):
                        implementer = hex(int(implementer))
                elif line.startswith('CPU part'):
                    if is_arm:
                        part = line.split(':')[1].strip().lower()
                        if not part.startswith('0x'):
                            part = hex(int(part))
                elif line.startswith('vendor_id'):
                    is_x86 = True
                    is_arm = False
                    vendor_id = line.split(':')[1].strip()
                elif line.startswith('model name'):
                    model_name = line.split(':', 1)[1].strip()

            # Catch last block if file doesn't end with newline
            if implementer and part:
                key = (implementer, part)
                if key not in cpus_found:
                    cpus_found[key] = 0
                cpus_found[key] += 1
            elif vendor_id and model_name:
                key = (vendor_id, model_name)
                if key not in cpus_found:
                    cpus_found[key] = 0
                cpus_found[key] += 1

    except FileNotFoundError:
        print("Error: /proc/cpuinfo not found. Is this a Linux system?")
        sys.exit(1)

    print(f"{'Core Count':<12} {'Vendor/Implementer':<20} {'Model':<30} {'Architecture'}")
    print("-" * 75)

    for key, count in cpus_found.items():
        if isinstance(key, tuple) and len(key) == 2:
            # ARM CPU
            imp, part = key
            if imp in arm_cpu_db and part in arm_cpu_db[imp]:
                model, arch = arm_cpu_db[imp][part]
                print(f"{count:<12} {imp:<20} {part:<10} {model:<30} {arch}")
            else:
                model = "Unknown"
                arch = "Unknown (AArch64)"
                print(f"{count:<12} {imp:<20} {part:<10} {model:<30} {arch}")
        else:
            # x86 CPU
            vendor_id, model_name = key
            architecture = "x86_64"

            # Try to match model name
            matched_model = "Unknown"
            if vendor_id in x86_cpu_db:
                for prefix, _ in x86_cpu_db[vendor_id]:
                    if prefix.lower() in model_name.lower():
                        matched_model = prefix
                        break

            print(f"{count:<12} {vendor_id:<20} {model_name:<30} {architecture}")

if __name__ == "__main__":
    get_cpu_architecture()