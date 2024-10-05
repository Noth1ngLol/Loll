import argparse
import json
import subprocess
import os
import tempfile
import sys
from typing import Dict, Any
from config_handler import ConfigHandler
from utils import logger, validate_file_path

RUST_BINARY = "./target/release/gguf_modifier"

def parse_arguments():
    parser = argparse.ArgumentParser(description="GGUF Metadata Manager")
    parser.add_argument("file_path", help="Path to the GGUF file")
    parser.add_argument("-C", action="store_true", help="Configure metadata")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-B", action="store_true", help="Basic configuration")
    group.add_argument("-a", action="store_true", help="Advanced configuration")
    parser.add_argument("--dry-run", action="store_true", help="Perform a dry run without modifying the file")
    parser.add_argument("--backup", action="store_true", help="Create a backup before modifying")
    parser.add_argument("--validate", action="store_true", help="Validate the GGUF file structure")
    parser.add_argument("-v", "--verbose", action="store_true", help="Increase output verbosity")
    return parser.parse_args()

def apply_configuration(file_path: str, config: Dict[str, Any], args):
    cmd = [RUST_BINARY, file_path, json.dumps(config)]
    
    if args.dry_run:
        cmd.append("--dry-run")
    if args.backup:
        cmd.append("--backup")
    if args.validate:
        cmd.append("--validate")
    if args.verbose:
        cmd.append("--verbose")

    logger.info(f"Executing Rust binary: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        logger.info("Configuration applied successfully!")
        logger.info(result.stdout)
    else:
        logger.error("Error applying configuration:")
        logger.error(result.stderr)
        sys.exit(1)

def main():
    args = parse_arguments()
    logger.set_verbose(args.verbose)

    file_path = validate_file_path(args.file_path)
    
    if args.C:
        config_handler = ConfigHandler(advanced=args.a)
        config = config_handler.create_default_config()
        logger.info("Default configuration created. Opening editor for modifications...")
        updated_config = config_handler.edit_config(config)
        
        logger.info("Applying configuration to GGUF file...")
        apply_configuration(file_path, updated_config, args)
    elif args.validate:
        apply_configuration(file_path, {}, args)
    else:
        logger.error("Please use the -C flag to configure metadata or --validate to validate the file.")
        sys.exit(1)

if __name__ == "__main__":
    main()
