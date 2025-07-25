#!/usr/bin/env python3
"""
Helper script for publishing vid-to-gif to PyPI.
"""

import os
import subprocess
import sys

def run_command(cmd, description):
    """Run a command and handle errors."""
    print(f"Running: {description}")
    try:
        result = subprocess.run(cmd, shell=True, check=True, text=True, 
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(result.stdout)
        if result.stderr:
            print(f"STDERR: {result.stderr}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running {description}: {e}")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        return False

def main():
    print("vid-to-gif PyPI Publishing Helper")
    print("==================================")
    
    # Check if we're in the right directory
    if not os.path.exists("vid_to_gif.py") or not os.path.exists("pyproject.toml"):
        print("Error: This script must be run from the project root directory")
        sys.exit(1)
    
    # Clean previous builds
    print("Cleaning previous builds...")
    run_command("rm -rf dist build *.egg-info", "Clean previous builds")
    
    # Build the package
    print("\nBuilding the package...")
    if not run_command("python -m build", "Build package"):
        print("Failed to build package")
        sys.exit(1)
    
    # List built files
    print("\nBuilt distributions:")
    run_command("ls -la dist/", "List built distributions")
    
    print("\nTo upload to TestPyPI:")
    print("  twine upload --repository testpypi dist/*")
    print("\nTo upload to PyPI:")
    print("  twine upload dist/*")
    print("\nTo test installation from TestPyPI:")
    print("  pip install --index-url https://test.pypi.org/simple/ vid-to-gif")

if __name__ == "__main__":
    main()