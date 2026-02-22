"""
Test script for pylint and flake8 for the Hotel Reservation System.

This module contains test cases to validate the code quality
using pylint and flake8.
"""

import subprocess


def run_linters():
    """Run pylint and flake8 on the source directory."""
    print("=== Running pylint ===")
    subprocess.run(["pylint", "source/"], check=False)

    print("\n=== Running flake8 ===")
    subprocess.run(["flake8", "source/"], check=False)


if __name__ == "__main__":
    run_linters()
