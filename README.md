# Klipper Toolchanger Tool Mapping

This repository provides a tool mapping for klipper-toolchanger.

**Note: This project is a work in progress. Features and configurations may change as development continues.**

**IMPORTANT!: Compatible with Moonraker v0.9.3-62**

## Installation

1. Add tool_mapping.cfg to your config (should be included after Tool_x.cfgs, so it overrides their Tx definitions)
2. Add variables.cfg to your config
3. Add toolchanger_metadata.py to moonraker/components directory.
4. Add [toolchanger_metadata] section below [file_manager] in moonraker.conf
5. Restart Klipper

## Configuration

Adjust tool_mapping.cfg and variables.cfg so it matches number of the tools in your machine.
Recommended to put SELECT_TOOL T=0 before homing in PRINT_START macro to ensure homing with tool 0 regardless of mapping.

## Usage

  RESET_TOOL_MAPPING - restores default mapping
  SET_TOOL_MAPPING T=x TOOL=y – Assigns command Tx to control physical tool y.

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## License

The GNU General Public License v3.0
