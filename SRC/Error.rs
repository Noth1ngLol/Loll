use std::fmt;
use std::io;

#[derive(Debug)]
pub enum GGUFError {
    Io(io::Error),
    InvalidMagic,
    UnsupportedVersion(u32),
    Json(serde_json::Error),
}

impl fmt::Display for GGUFError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match self {
            GGUFError::Io(err) => write!(f, "I/O error: {}", err),
            GGUFError::InvalidMagic => write!(f, "Invalid GGUF magic number"),
            GGUFError::UnsupportedVersion(v) => write!(f, "Unsupported GGUF version: {}", v),
            GGUFError::Json(err) => write!(f, "JSON error: {}", err),
        }
    }
}

impl std::error::Error for GGUFError {}

impl From<io::Error> for GGUFError {
    fn from(err: io::Error) -> GGUFError {
        GGUFError::Io(err)
    }
}

impl From<serde_json::Error> for GGUFError {
    fn from(err: serde_json::Error) -> GGUFError {
        GGUFError::Json(err)
    }
}

pub type Result<T> = std::result::Result<T, GGUFError>;
