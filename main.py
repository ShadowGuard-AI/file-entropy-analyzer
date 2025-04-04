import argparse
import logging
import math
import os
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def calculate_entropy(file_path):
    """
    Calculates the entropy of a file.

    Args:
        file_path (Path): The path to the file.

    Returns:
        float: The entropy of the file, or None if an error occurs.
    """
    try:
        with open(file_path, "rb") as f:
            data = f.read()
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        return None
    except Exception as e:
        logging.error(f"Error reading file: {e}")
        return None

    if not data:
        logging.warning("File is empty. Entropy is 0.")
        return 0.0

    entropy = 0
    data_len = len(data)
    if data_len > 0:  # Avoid ZeroDivisionError
      byte_counts = {}
      for byte in data:
          if byte in byte_counts:
              byte_counts[byte] += 1
          else:
              byte_counts[byte] = 1

      for count in byte_counts.values():
          probability = float(count) / data_len
          entropy -= probability * math.log(probability, 2)

    return entropy


def setup_argparse():
    """
    Sets up the argument parser for the command line interface.

    Returns:
        argparse.ArgumentParser: The argument parser.
    """
    parser = argparse.ArgumentParser(description="Calculates the entropy of a file.")
    parser.add_argument("file_path", type=str, help="The path to the file to analyze.")
    return parser


def main():
    """
    Main function to calculate and display the entropy of a file.
    """
    parser = setup_argparse()
    args = parser.parse_args()

    file_path = Path(args.file_path)

    # Input Validation: check if the file exists
    if not file_path.exists():
        logging.error(f"File does not exist: {file_path}")
        return

    # Input Validation: Check if file is a file and not a directory or symlink, etc.
    if not file_path.is_file():
      logging.error(f"Not a regular file: {file_path}")
      return

    entropy = calculate_entropy(file_path)

    if entropy is not None:
        print(f"Entropy of {file_path}: {entropy:.4f}")

        # Interpretation of Entropy
        if entropy > 7.5:
            print("High entropy: The file may be compressed or encrypted.")
        elif entropy > 6.0:
            print("Medium entropy: The file may contain some form of structured data.")
        else:
            print("Low entropy: The file may contain mostly text or uncompressed data.")


if __name__ == "__main__":
    # Usage Examples:
    # To run this script:
    # 1. Save it as entropy_analyzer.py
    # 2. Run it from the command line: python entropy_analyzer.py <file_path>
    # Example: python entropy_analyzer.py example.txt

    main()