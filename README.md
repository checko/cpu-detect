# CPU Architecture Detection Tool

A modular Python tool for identifying host CPU architecture and family on Linux and Windows systems.

## Features

- **Cross-Platform Support**: Works on both Linux and Windows systems
- **Multi-Architecture Support**: Detects both ARM and x86 CPUs
- **Detailed Information**: Provides core counts, model names, and architecture details
- **Modular Design**: Clean separation of concerns with dedicated modules
- **Error Handling**: Robust error handling and validation

## Architecture

The tool is organized into several modules:

- `cpu_database.py`: Contains CPU model databases for ARM and x86 architectures
- `cpuinfo_parser.py`: Handles parsing of CPU information on Linux and Windows
- `cpu_detector.py`: Orchestrates CPU detection and identification
- `output_formatter.py`: Formats and displays results
- `check_arm_arch.py`: Main entry point

## Usage

```bash
python3 check_arm_arch.py
```

### Example Output

**x86 System:**
```
Core Count   Vendor/Implementer   Model                          Architecture
--------------------------------------------------------------------------------
32           AuthenticAMD         AMD Ryzen 9 9950X3D 16-Core Processor x86_64
```

**ARM System:**
```
Core Count   Vendor/Implementer   Model                          Architecture
--------------------------------------------------------------------------------
8            0x41                 0xd87      Cortex-A725         ARMv9.2-A
```

## Installation

No installation required! Just clone the repository and run the script:

```bash
git clone https://github.com/checko/cpu-detect.git
cd cpu-detect
python3 check_arm_arch.py
```

## Requirements

- Python 3.6+
- Linux or Windows operating system
- On Windows: `wmic` command (available by default)
- On Linux: Access to `/proc/cpuinfo` (standard on Linux systems)

## Supported CPUs

### ARM CPUs
- **Cortex Series**: A35, A53, A55, A57, A65, A72, A73, A75, A76, A77, A78, A78C, A510, A710, A520, A720, A725
- **Cortex-X Series**: X1, X2, X3, X4, X925
- **Neoverse Series**: N1, N2, V1, E1
- **Other**: Various ARM-based processors from multiple vendors

### x86 CPUs
- **Intel**: Core i3/i5/i7/i9 series, Xeon, Atom, Celeron, Pentium
- **AMD**: Ryzen, Phenom, Athlon, EPYC, A-Series, FX-Series
- **Other x86 vendors**: Generic x86_64 support

## Error Handling

The tool includes comprehensive error handling for:
- Unsupported platforms
- Missing system files or commands
- Malformed CPU information
- Unknown CPU models

## Contributing

To add support for new CPU models:

1. Update the appropriate database class in `cpu_database.py`
2. Add new entries to the database dictionaries
3. Test with your specific CPU model

## Project Structure

```
cpu-detect/
├── .gitignore              # Python .gitignore rules
├── README.md               # This documentation
├── check_arm_arch.py       # Main entry point script
├── cpu_database.py         # CPU model databases (ARM & x86)
├── cpu_detector.py         # CPU detection orchestration
├── cpuinfo_parser.py       # Cross-platform CPU info parsing
└── output_formatter.py     # Output formatting and display
```

## License

This project is open source and available under the MIT License.