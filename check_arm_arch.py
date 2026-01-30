#!/usr/bin/env python3
import sys

def get_cpu_architecture():
    # Mapping of CPU Implementer -> CPU Part -> (Model Name, Architecture)
    # 0x41 is ARM Limited.
    cpu_db = {
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
            '0xd40': ('Neoverse V1', 'ARMv8.4-A'), # often cited as v8.4 or v8.6
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
            '0xd4e': ('Cortex-X4', 'ARMv9.2-A'), # Early X4 ID
            '0xd80': ('Cortex-A520', 'ARMv9.2-A'),
            '0xd81': ('Cortex-A720', 'ARMv9.2-A'),
            '0xd82': ('Cortex-X4', 'ARMv9.2-A'),
            '0xd84': ('Cortex-A525', 'ARMv9.2-A'),
            '0xd85': ('Cortex-X925', 'ARMv9.2-A'),
            '0xd87': ('Cortex-A725', 'ARMv9.2-A'),
        },
        # Apple, Qualcomm, Samsung, etc. have their own IDs, 
        # but linux typically reports 0x41 (ARM) for the reference designs.
    }

    cpus_found = {}

    try:
        with open('/proc/cpuinfo', 'r') as f:
            implementer = None
            part = None
            
            for line in f:
                line = line.strip()
                if not line:
                    # End of a processor block, save what we found
                    if implementer and part:
                        key = (implementer, part)
                        if key not in cpus_found:
                            cpus_found[key] = 0
                        cpus_found[key] += 1
                    implementer = None
                    part = None
                    continue

                if line.startswith('CPU implementer'):
                    implementer = line.split(':')[1].strip().lower()
                    # Ensure hex format 0x...
                    if not implementer.startswith('0x'):
                        implementer = hex(int(implementer))
                elif line.startswith('CPU part'):
                    part = line.split(':')[1].strip().lower()
                    if not part.startswith('0x'):
                        part = hex(int(part))
            
            # Catch last block if file doesn't end with newline
            if implementer and part:
                key = (implementer, part)
                if key not in cpus_found:
                    cpus_found[key] = 0
                cpus_found[key] += 1

    except FileNotFoundError:
        print("Error: /proc/cpuinfo not found. Is this a Linux system?")
        sys.exit(1)

    print(f"{'Core Count':<12} {'Implementer':<12} {'Part':<10} {'Model':<20} {'Architecture'}")
    print("-" * 70)

    for (imp, part), count in cpus_found.items():
        details = cpu_db.get(imp, {}).get(part)
        
        if details:
            model, arch = details
        else:
            model = "Unknown"
            arch = "Unknown (AArch64)"
        
        print(f"{count:<12} {imp:<12} {part:<10} {model:<20} {arch}")

if __name__ == "__main__":
    get_cpu_architecture()
