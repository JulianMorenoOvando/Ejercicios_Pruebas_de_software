# pylint: disable=C0103
"""
Word Count Program
This script reads words from a file and identifies their frequency
using basic algorithms.
"""

import sys
import time
import os


def get_words_from_file(file_path):
    """Reads a file and extracts words, handling errors."""
    words = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                # Basic algorithm to split words manually if needed,
                # but split() is generally acceptable as a basic string op.
                # However, to be strictly 'basic algorithm':
                word = ""
                for char in line:
                    if char.isspace():
                        if word:
                            words.append(word)
                            word = ""
                    else:
                        word += char
                if word:
                    words.append(word)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)
    except UnicodeDecodeError as e:
        print(f"Encoding error: {e}")
        sys.exit(1)
    except OSError as e:
        print(f"I/O error: {e}")
        sys.exit(1)
    return words


def count_frequencies(words):
    """Counts the frequency of each word using a basic dictionary algorithm."""
    frequencies = {}
    for word in words:
        if word in frequencies:
            frequencies[word] += 1
        else:
            frequencies[word] = 1
    return frequencies


def main():
    """Main function to execute the word count."""
    if len(sys.argv) < 2:
        print("Usage: python wordCount.py fileWithData.txt")
        sys.exit(1)

    file_path = sys.argv[1]
    start_time = time.time()

    words = get_words_from_file(file_path)

    if not words:
        print("No words found in the file.")
        elapsed_time = time.time() - start_time
        print(f"Execution Time: {elapsed_time:.4f} seconds")
        sys.exit(0)

    frequencies = count_frequencies(words)
    elapsed_time = time.time() - start_time

    # Sort results by frequency or word? Req doesn't specify.
    # I'll sort by word for a clean output.
    sorted_words = sorted(frequencies.keys())

    results = [
        "--- Word Count Results ---",
        f"File: {file_path}",
        f"{'Word':<20} {'Frequency':<10}",
        "-" * 31
    ]

    for word in sorted_words:
        results.append(f"{word:<20} {frequencies[word]:<10}")

    results.append("-" * 31)
    results.append(f"Execution Time: {elapsed_time:.4f} seconds")

    # Print to screen
    for line in results:
        print(line)

    # Write to file in results directory, if exists it will be appended
    try:
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # Go up one level to project directory (P3) and then to results
        results_dir = os.path.join(script_dir, "..", "results")
        # Create results directory if it doesn't exist
        os.makedirs(results_dir, exist_ok=True)
        # Create the output file path
        output_file = os.path.join(results_dir, "WordCountResults.txt")
        with open(output_file, "a", encoding="utf-8") as out_file:
            for line in results:
                out_file.write(line + "\n")
        print(f"\nResults written to: {os.path.abspath(output_file)}")
    except IOError as e:
        print(f"Error writing to file: {e}")


if __name__ == "__main__":
    main()
