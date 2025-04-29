#!/usr/bin/env python3
"""
Script for using AutoGen code agent
"""

import argparse
import sys

try:
    from bmt_libs.agents.autogen.core import CodeAgent
except ImportError:
    print(
        "Error: AutoGen is not available. Install with: pip install 'bmt-scripts[agents]'"
    )
    sys.exit(1)


def main():
    """Main function for AutoGen code agent"""
    parser = argparse.ArgumentParser(description="AutoGen Code Agent")
    parser.add_argument("prompt", type=str, help="Code task description")

    args = parser.parse_args()

    print("Initializing code agent...")
    agent = CodeAgent()

    print(f"Processing request: {args.prompt}")
    result = agent.write_code(args.prompt)

    print("\nGenerated code:")
    print(result)


if __name__ == "__main__":
    main()
