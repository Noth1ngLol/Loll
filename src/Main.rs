mod gguf_modifier;
mod error;

use std::env;
use std::path::Path;
use serde_json::Value;
use crate::gguf_modifier::GGUFModifier;
use crate::error::Result;

fn main() -> Result<()> {
    let args: Vec<String> = env::args().collect();
    if args.len() < 3 {
        eprintln!("Usage: {} <file_path> <json_config> [--dry-run] [--backup] [--validate] [--verbose]", args[0]);
        std::process::exit(1);
    }

    let file_path = Path::new(&args[1]);
    let config_json = &args[2];
    let dry_run = args.contains(&"--dry-run".to_string());
    let backup = args.contains(&"--backup".to_string());
    let validate = args.contains(&"--validate".to_string());
    let verbose = args.contains(&"--verbose".to_string());

    let mut modifier = GGUFModifier::new(file_path, verbose)?;

    if validate {
        modifier.validate_structure()?;
        println!("GGUF file structure is valid.");
        return Ok(());
    }

    if backup {
        modifier.create_backup()?;
    }

    let config: Value = serde_json::from_str(config_json)?;

    if dry_run {
        println!("Dry run: The following changes would be made:");
        for (key, value) in config.as_object().unwrap() {
            println!("  {} -> {:?}", key, value);
        }
    } else {
        modifier.update_metadata(config)?;
        println!("GGUF metadata modified successfully");
    }

    Ok(())
}
