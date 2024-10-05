import json
import tempfile
import os
import subprocess
from typing import Dict, Any
from utils import logger

class ConfigHandler:
    def __init__(self, advanced: bool = False):
        self.advanced = advanced

    def create_default_config(self) -> Dict[str, Any]:
        basic_config = {
            "model_name": "My GGUF Model",
            "model_type": "llama",
            "context_length": 2048,
            "vocab_size": 32000,
            "embedding_length": 4096
        }
        
        if not self.advanced:
            return basic_config
        
        advanced_config = {
            **basic_config,
            "quantization_method": "q4_0",
            "use_gpu": True,
            "temperature": 0.7,
            "top_p": 0.9,
            "top_k": 40,
            "repeat_penalty": 1.1,
            "num_layers": 32,
            "num_heads": 32,
            "key_length": 128,
            "value_length": 128,
            "feed_forward_length": 11008,
            "rope_scaling_type": "linear",
            "rope_scaling_factor": 1.0
        }
        
        return advanced_config

    def edit_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        with tempfile.NamedTemporaryFile(mode='w+', suffix='.json', delete=False) as temp_file:
            json.dump(config, temp_file, indent=2)
            temp_file_path = temp_file.name

        editor = os.environ.get('EDITOR', 'nano')
        subprocess.call([editor, temp_file_path])

        try:
            with open(temp_file_path, 'r') as temp_file:
                updated_config = json.load(temp_file)
        except json.JSONDecodeError:
            logger.error("Invalid JSON in the configuration file. Using the original configuration.")
            updated_config = config
        finally:
            os.unlink(temp_file_path)

        return updated_config
