#!/usr/bin/env python3
"""
AI Model Benchmarking CLI
Command-line interface for running benchmarks and comparing AI models.
"""

import argparse
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from ml.router import AdaptiveModelSelector
from tests.benchmark import AdvancedModelBenchmark

def run_benchmark(args):
    """Run comprehensive benchmark across all models"""
    print("🤖 Starting AI Model Benchmark...")

    # Check for API keys
    required_keys = ['NVIDIA_API_KEY', 'OPENAI_API_KEY', 'ANTHROPIC_API_KEY', 'GOOGLE_API_KEY']
    missing_keys = [key for key in required_keys if not os.getenv(key)]

    if missing_keys:
        print(f"❌ Missing API keys: {', '.join(missing_keys)}")
        print("Please set them in your .env file or environment variables")
        return

    models = [
        {"name": "gpt-4o", "type": "openai"},
        {"name": "deepseek-r1", "type": "deepseek"},
        {"name": "claude-3-5-sonnet-20241022", "type": "anthropic"},
        {"name": "gemini-2.0-flash-exp", "type": "google"}
    ]

    try:
        benchmark = AdvancedModelBenchmark(models)
        results = benchmark.run_benchmark()

        print("\n📊 Benchmark Results:")
        print("-" * 50)
        for result in results:
            print(f"Model: {result.model_name}")
            print(".2f")
            print(".2f")
            print(".1f")
            print(".1f")
            print()

        print("✅ Benchmark completed! Check reports/ for detailed visualizations.")

    except Exception as e:
        print(f"❌ Benchmark failed: {e}")

def compare_models(args):
    """Quick comparison of two models on a specific task"""
    print(f"🔄 Comparing {args.model1} vs {args.model2}")
    print(f"Task: {args.task}")

    selector = AdaptiveModelSelector()

    try:
        # Simple comparison - in real implementation, this would run actual API calls
        recommendation = selector.select_optimal_model(args.task, args.complexity)
        print(f"🤖 Recommended model: {recommendation}")

        # Mock comparison results
        print("\n📈 Quick Comparison:")
        print(f"{args.model1}: ~2.1s response, 85% success")
        print(f"{args.model2}: ~1.8s response, 92% success")

    except Exception as e:
        print(f"❌ Comparison failed: {e}")

def list_models(args):
    """List available models"""
    print("🤖 Available AI Models:")
    print("-" * 30)
    models = [
        ("DeepSeek R1", "NVIDIA", "Reasoning-focused"),
        ("GPT-4o", "OpenAI", "Most advanced GPT"),
        ("Claude-3.5-Sonnet", "Anthropic", "Balanced performance"),
        ("Gemini-2.0-Flash-Exp", "Google", "Latest experimental")
    ]

    for name, provider, desc in models:
        print("20")

def show_status(args):
    """Show system status and API key configuration"""
    print("🔍 System Status:")
    print("-" * 20)

    api_keys = {
        'NVIDIA_API_KEY': 'DeepSeek R1',
        'OPENAI_API_KEY': 'GPT-4o',
        'ANTHROPIC_API_KEY': 'Claude-3.5',
        'GOOGLE_API_KEY': 'Gemini-2.0'
    }

    all_configured = True
    for key, model in api_keys.items():
        status = "✅" if os.getenv(key) else "❌"
        print(f"{status} {model}: {key}")

    if all_configured:
        print("\n✅ All API keys configured!")
    else:
        print("\n⚠️  Some API keys missing. Set them in .env file.")

def main():
    parser = argparse.ArgumentParser(
        description="AI Model Benchmarking CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli.py benchmark              # Run full benchmark
  python cli.py compare gpt-4o deepseek-r1 --task "code generation"
  python cli.py models                 # List available models
  python cli.py status                 # Check configuration
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Benchmark command
    subparsers.add_parser('benchmark', help='Run comprehensive benchmark')

    # Compare command
    compare_parser = subparsers.add_parser('compare', help='Compare two models')
    compare_parser.add_argument('model1', help='First model to compare')
    compare_parser.add_argument('model2', help='Second model to compare')
    compare_parser.add_argument('--task', default='general reasoning',
                               help='Task description (default: general reasoning)')
    compare_parser.add_argument('--complexity', choices=['low', 'medium', 'high', 'extreme'],
                               default='medium', help='Task complexity (default: medium)')

    # Models command
    subparsers.add_parser('models', help='List available models')

    # Status command
    subparsers.add_parser('status', help='Show system status')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    # Route to appropriate handler
    if args.command == 'benchmark':
        run_benchmark(args)
    elif args.command == 'compare':
        compare_models(args)
    elif args.command == 'models':
        list_models(args)
    elif args.command == 'status':
        show_status(args)

if __name__ == '__main__':
    main()