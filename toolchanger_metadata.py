# Original GCode metadata extraction utility
# Copyright (C) 2020-2025 Eric Callahan <arksine.code@gmail.com>
#
# Original METADATA_SCRIPT switching:
# Copyright (C) 2022-2025  moggieuk#6538 (discord)
#                          moggieuk@hotmail.com
#
# This file may be distributed under the terms of the GNU GPLv3 license.
#
from __future__ import annotations
import json
import logging, os, sys
import argparse, traceback

# Annotation imports
from typing import (
    TYPE_CHECKING,
    Any,
    Optional,
    Dict,
    List,
    Tuple,
    Type,
)
if TYPE_CHECKING:
    pass
    
logging.basicConfig(stream=sys.stderr, level=logging.INFO)
logger = logging.getLogger("metadata")

class ToolchangerMetadata:
    def __init__(self, config: ConfigHelper):
        self.config = config
       
        self.extend_metadata_script(config)

    def extend_metadata_script(self, config):
        from .file_manager import file_manager
        file_manager.METADATA_SCRIPT = os.path.abspath(__file__)

def load_component(config):
    return ToolchangerMetadata(config)
    
def parse_filament_used_mm(self) -> Optional[str]:
    return metadata.regex_find_string(r'; filament used \[mm\] = (%S)', self.footer_data).replace(',', ';')
    
def parse_filament_colors(self) -> Optional[str]:
    return metadata.regex_find_string(r'; filament_colour = (%S)', self.footer_data)
    
def parse_total_toolchanges(self) -> Optional[float]:
    totalToolchanges = metadata.regex_find_int(r"; total filament change = (%D)", self.footer_data)
    if totalToolchanges is not None:
        return totalToolchanges
    else:
        return metadata.regex_find_int(r"; total toolchanges = (%D)", self.footer_data)

if __name__ == "__main__":

    directory = os.path.dirname(os.path.abspath(__file__))
    target_dir = directory + "/file_manager"
    os.chdir(target_dir)
    sys.path.insert(0, target_dir)
    
    import metadata

    parser = argparse.ArgumentParser(
        description="GCode Metadata Extraction Utility")
    parser.add_argument(
        "-c", "--config", metavar='<config_file>', default=None,
        help="Optional json configuration file for metadata.py"
    )
    parser.add_argument(
        "-f", "--filename", metavar='<filename>', default=None,
        help="name gcode file to parse")
    parser.add_argument(
        "-p", "--path", metavar='<path>', default=None,
        help="optional path to folder containing the file"
    )
    parser.add_argument(
        "-u", "--ufp", metavar="<ufp file>", default=None,
        help="optional path of ufp file to extract"
    )
    parser.add_argument(
        "-o", "--check-objects", dest='check_objects', action='store_true',
        help="process gcode file for exclude opbject functionality")
    args = parser.parse_args()
    config: Dict[str, Any] = {}
    if args.config is None:
        if args.filename is None:
            logger.info(
                "The '--filename' (-f) option must be specified when "
                " --config is not set"
            )
            sys.exit(-1)
        config["filename"] = args.filename
        config["gcode_dir"] = args.path
        config["ufp_path"] = args.ufp
        config["check_objects"] = args.check_objects
    else:
        # Config file takes priority over command line options
        try:
            with open(args.config, "r") as f:
                config = (json.load(f))
        except Exception:
            logger.info(traceback.format_exc())
            sys.exit(-1)
        if config.get("filename") is None:
            logger.info("The 'filename' field must be present in the configuration")
            sys.exit(-1)
    if config.get("gcode_dir") is None:
        config["gcode_dir"] = os.path.abspath(os.path.dirname(__file__))
        
    toolchanger_data = [
        'filament_used_mm',
        'filament_colors',
        'total_toolchanges'
    ]
    
    supported_data = set(metadata.SUPPORTED_DATA)
    metadata.SUPPORTED_DATA.extend(item for item in toolchanger_data if item not in supported_data)
        
    metadata.PrusaSlicer.parse_filament_used_mm = parse_filament_used_mm
    metadata.PrusaSlicer.parse_filament_colors = parse_filament_colors
    metadata.PrusaSlicer.parse_total_toolchanges = parse_total_toolchanges

    metadata.main(config)
