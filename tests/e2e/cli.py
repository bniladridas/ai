import os
import subprocess
import sys
from pathlib import Path


def test_cli_help():
    """Test CLI help output"""
    cli_path = Path(__file__).parent.parent.parent / 'cli.py'
    result = subprocess.run([sys.executable, str(cli_path), '--help'],
                          capture_output=True, text=True)
    assert result.returncode == 0
    assert 'ai benchmark cli' in result.stdout.lower()

def test_cli_status():
    """Test CLI status command"""
    cli_path = Path(__file__).parent.parent.parent / 'cli.py'
    result = subprocess.run([sys.executable, str(cli_path), 'status'],
                          capture_output=True, text=True)
    assert result.returncode == 0
    assert 'deepseek r1:' in result.stdout.lower()

def test_cli_models():
    """Test CLI models command"""
    cli_path = Path(__file__).parent.parent.parent / 'cli.py'
    result = subprocess.run([sys.executable, str(cli_path), 'models'],
                          capture_output=True, text=True)
    assert result.returncode == 0
    assert 'deepseek r1' in result.stdout.lower()
    assert 'gpt-4o' in result.stdout.lower()

def test_cli_compare():
    """Test CLI compare command"""
    cli_path = Path(__file__).parent.parent.parent / 'cli.py'
    result = subprocess.run([sys.executable, str(cli_path), 'compare', 'gpt-4o', 'deepseek-r1'],
                          capture_output=True, text=True)
    assert result.returncode == 0
    assert 'recommended:' in result.stdout.lower()

def test_cli_benchmark_missing_keys():
    """Test CLI benchmark with missing API keys"""
    # Temporarily clear API keys
    original_env = {}
    keys_to_clear = ['NVIDIA_API_KEY', 'OPENAI_API_KEY', 'ANTHROPIC_API_KEY', 'GOOGLE_API_KEY']
    for key in keys_to_clear:
        original_env[key] = os.environ.get(key)
        os.environ.pop(key, None)

    try:
        cli_path = Path(__file__).parent.parent.parent / 'cli.py'
        result = subprocess.run([sys.executable, str(cli_path), 'benchmark'],
                              capture_output=True, text=True)
        assert result.returncode == 0
        assert 'missing api keys' in result.stdout.lower()
    finally:
        # Restore original environment
        for key, value in original_env.items():
            if value is not None:
                os.environ[key] = value

def test_cli_invalid_command():
    """Test CLI with invalid command"""
    cli_path = Path(__file__).parent.parent.parent / 'cli.py'
    result = subprocess.run([sys.executable, str(cli_path), 'invalid'],
                          capture_output=True, text=True)
    assert result.returncode == 2  # argparse exits with 2 for invalid choice

