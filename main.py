import argparse
import logging
import math
import os
import sys
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
            # The file is read whole. Entropy needs every byte counted anyway,
            # but a chunked count would give the same number without holding a
            # very large file in memory at once.
            data = f.read()
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        return None
    except Exception as e:
        logging.error(f"Error reading file: {e}")
        return None

    if not data:
        logging.error("File is empty: no data to analyze.")
        return None

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
          # This is one Shannon entropy figure for the whole file, byte values
          # only. Position and structure play no part, so a small encrypted or
          # compressed region inside a large plain file is diluted by everything
          # around it and the total can still read as low. There is no per block
          # breakdown to catch that case.
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
        sys.exit(1)

    # Input Validation: Check if file is a file and not a directory or symlink, etc.
    # is_file follows symlinks, so a link to a regular file passes this
    # check, whatever the wording above it suggests. The target is what
    # gets measured, under the link's name in the printed line.
    if not file_path.is_file():
      logging.error(f"Not a regular file: {file_path}")
      sys.exit(1)

    entropy = calculate_entropy(file_path)

    if entropy is None:
        sys.exit(1)

    if entropy is not None:
        print(f"Entropy of {file_path}: {entropy:.4f}")

        # Interpretation of Entropy
        # The three bands are rules of thumb printed as interpretation, not
        # verdicts. Compressed data that is mostly padding can land in the
        # medium band, and dense executable code can cross into high.
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