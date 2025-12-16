#!/usr/bin/env python3
"""
Data validation utility for benchmarking configurations.
"""

import sys
from pathlib import Path

import yaml


def validate_config(config_path):
    """Validate the benchmark configuration file."""
    if not config_path.exists():
        print(f"Error: Config file {config_path} not found.")
        return False

    try:
        with open(config_path) as f:
            config = yaml.safe_load(f)
    except yaml.YAMLError as e:
        print(f"Error parsing YAML: {e}")
        return False

    models = config.get("models", [])
    if not models:
        print("Error: No models defined in config.")
        return False

    for model in models:
        if not all(key in model for key in ["name", "type"]):
            print(f"Error: Model missing required fields: {model}")
            return False

    print("Config validation passed.")
    return True


def main():
    config_path = Path(__file__).parent.parent / "config" / "benchmark.yaml"
    if not validate_config(config_path):
        sys.exit(1)


if __name__ == "__main__":
    main()
