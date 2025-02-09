# Klipper Toolchanger Tool Mapping

This repository provides a tool mapping for klipper-toolchanger.

**Note: This project is a work in progress. Features and configurations may change as development continues.**

## Installation

1. Add tool_mapping.cfg to your config
2. Add variables.cfg to your config
3. Replace Moonraker's metadata.py
4. Restart Klipper

## Configuration

Adjust tool_mapping.cfg and variables.cfg so it matches number of the tools in your machine.
Recommended to put SELECT_TOOL T=0 before homing in PRINT_START macro to ensure homing with tool 0 regardless of mapping.

## Usage

RESET_TOOL_MAPPING - restores default mapping
SET_TOOL_MAPPING T=<x> TOOL=<y> – Assigns command T<x> to control physical tool <y>.

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## License

The GNU General Public License v3.0
