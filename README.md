# CPU Architecture Detection Tool

A modular Python tool for identifying host CPU architecture and family on Linux and Windows systems.

## Features

- **Multi-Architecture Support**: Detects both ARM and x86 CPUs
- **Detailed Information**: Provides core counts, model names, and architecture details
- **Modular Design**: Clean separation of concerns with dedicated modules
- **Error Handling**: Robust error handling and validation
- **Linux Focused**: Optimized for Linux systems using `/proc/cpuinfo`

## Architecture

The tool is organized into several modules:

- `cpu_database.py`: Contains CPU model databases for ARM and x86 architectures
- `cpuinfo_parser.py`: Handles parsing of `/proc/cpuinfo` file
- `cpu_detector.py`: Orchestrates CPU detection and identification
- `output_formatter.py`: Formats and displays results
- `check_arm_arch.py`: Main entry point

## Usage

```bash
python3 check_arm_arch.py
```

### Example Output

```
Core Count   Vendor/Implementer   Model                          Architecture
--------------------------------------------------------------------------------
32           AuthenticAMD         AMD Ryzen 9 9950X3D 16-Core Processor x86_64
```

## Requirements

- Python 3.6+
- Linux or Windows operating system

## Supported CPUs

### ARM CPUs
- Cortex-A53, A35, A55, A65, A57, A72, A73, A75, A76, A77, A78, A78C
- Cortex-X1, X2, X3, X4
- Neoverse N1, N2, V1, E1
- And more...

### x86 CPUs
- Intel Core i3/i5/i7/i9
- Intel Xeon, Atom, Celeron
- AMD Ryzen, Phenom, Athlon, EPYC, A-Series

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

## License

This project is open source and available under the MIT License.