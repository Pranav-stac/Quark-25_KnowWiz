import pytest
import sys

def main():
    """Run the test suite"""
    exit_code = pytest.main(["tests/", "-v"])
    sys.exit(exit_code)

if __name__ == "__main__":
    main() 