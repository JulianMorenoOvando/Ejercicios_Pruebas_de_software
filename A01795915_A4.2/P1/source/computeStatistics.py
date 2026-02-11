# pylint: disable=C0103
"""
Compute Statistics Program
This script reads numbers from a file and computes descriptive statistics:
mean, median, mode, standard deviation, and variance.
"""

import sys
import time
import os


def get_numbers_from_file(file_path):
    """Reads a file and extracts numbers, handling errors."""
    numbers = []
    errors = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                try:
                    numbers.append(float(line))
                except ValueError:
                    errors.append(line)
                    print(f"Error: Invalid data found: '{line}'")
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)
    return numbers, errors


def compute_mean(data):
    """Calculates the mean of a list of numbers."""
    if not data:
        return 0
    total = 0.0
    for x in data:
        total += x
    return total / len(data)


def compute_median(data):
    """Calculates the median of a list of numbers."""
    if not data:
        return 0
    sorted_data = sorted(data)
    n = len(sorted_data)
    mid = n // 2
    if n % 2 == 0:
        return (sorted_data[mid - 1] + sorted_data[mid]) / 2
    return sorted_data[mid]


def compute_mode(data):
    """Calculates the mode(s) of a list of numbers."""
    if not data:
        return 0
    counts = {}
    for x in data:
        counts[x] = counts.get(x, 0) + 1

    max_count = 0
    for count in counts.values():
        max_count = max(max_count, count)

    modes = [val for val, count in counts.items() if count == max_count]

    if len(modes) == len(data) and len(data) > 1:
        return "No unique mode"
    return modes[0] if len(modes) == 1 else modes


def compute_variance(data, mean):
    """Calculates the population variance."""
    if not data:
        return 0
    sum_sq_diff = 0.0
    for x in data:
        sum_sq_diff += (x - mean) ** 2
    return sum_sq_diff / len(data)


def compute_std_dev(variance):
    """Calculates the standard deviation."""
    return variance ** 0.5


def print_console_output(file_path, stats_dict, elapsed_time):
    """Print statistics results to console."""
    print("--- Statistics Results ---")
    print(f"File: {file_path}")
    print(f"Count: {stats_dict['count']}")
    print(f"Mean: {stats_dict['mean']:.4f}")
    print(f"Median: {stats_dict['median']:.4f}")
    print(f"Mode: {stats_dict['mode']}")
    print(f"Standard Deviation: {stats_dict['std_dev']:.4f}")
    print(f"Variance: {stats_dict['variance']:.4f}")
    if stats_dict.get('errors'):
        print(f"Errors: {stats_dict['errors']}")
    print(f"Execution Time: {elapsed_time:.4f} seconds")


def format_mode_for_table(mode):
    """Format mode value for table output."""
    if isinstance(mode, list):
        return str(mode[0]) if len(mode) == 1 else str(mode[0])
    if mode == "No unique mode":
        return "#N/A"
    return str(mode)


def read_existing_table(output_file):
    """Read existing table data from file if it exists."""
    table_data = {
        'TC': ['TC'],
        'COUNT': ['COUNT'],
        'MEAN': ['MEAN'],
        'MEDIAN': ['MEDIAN'],
        'MODE': ['MODE'],
        'SD': ['SD'],
        'VARIANCE': ['VARIANCE']
    }

    if os.path.exists(output_file):
        with open(output_file, "r", encoding="utf-8") as in_file:
            lines = in_file.readlines()
            if len(lines) >= 7:
                # Parse existing table
                for i, key in enumerate(['TC', 'COUNT', 'MEAN', 'MEDIAN',
                                        'MODE', 'SD', 'VARIANCE']):
                    table_data[key] = lines[i].strip().split('\t')

    return table_data


def write_table_to_file(file_path, stats_dict):
    """Write statistics to file in tab-separated table format."""
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Go up one level to project directory (P1) and then to results
    results_dir = os.path.join(script_dir, "..", "results")
    # Create results directory if it doesn't exist
    os.makedirs(results_dir, exist_ok=True)
    # Create the output file path
    output_file = os.path.join(results_dir, "StatisticsResults.txt")

    # Extract test case name from file path
    file_name = os.path.basename(file_path)
    tc_name = os.path.splitext(file_name)[0]

    # Format mode for table output
    mode_str = format_mode_for_table(stats_dict['mode'])

    # Read existing table if it exists
    table_data = read_existing_table(output_file)

    # Append new column
    table_data['TC'].append(tc_name)
    table_data['COUNT'].append(str(stats_dict['count']))
    table_data['MEAN'].append(f"{stats_dict['mean']:.10g}")
    table_data['MEDIAN'].append(f"{stats_dict['median']:.10g}")
    table_data['MODE'].append(mode_str)
    table_data['SD'].append(f"{stats_dict['std_dev']:.10g}")
    table_data['VARIANCE'].append(f"{stats_dict['variance']:.10g}")

    # Write the updated table
    with open(output_file, "w", encoding="utf-8") as out_file:
        for key in ['TC', 'COUNT', 'MEAN', 'MEDIAN', 'MODE', 'SD', 'VARIANCE']:
            out_file.write('\t'.join(table_data[key]) + '\n')

    print(f"\nResults written to: {os.path.abspath(output_file)}")


def main():
    """Main function to execute the statistics computation."""
    if len(sys.argv) < 2:
        print("Usage: python computeStatistics.py fileWithData.txt")
        sys.exit(1)

    file_path = sys.argv[1]
    start_time = time.time()

    data, errors = get_numbers_from_file(file_path)

    if not data:
        print("No valid numbers found in the file.")
        elapsed_time = time.time() - start_time
        print(f"Execution Time: {elapsed_time:.4f} seconds")
        sys.exit(0)

    mean = compute_mean(data)
    median = compute_median(data)
    mode = compute_mode(data)
    variance = compute_variance(data, mean)
    std_dev = compute_std_dev(variance)

    elapsed_time = time.time() - start_time

    # Create statistics dictionary
    stats = {
        'count': len(data),
        'mean': mean,
        'median': median,
        'mode': mode,
        'std_dev': std_dev,
        'variance': variance,
        'errors': errors
    }

    # Print to screen (console output)
    print_console_output(file_path, stats, elapsed_time)

    # Write to file in tab-separated table format
    try:
        write_table_to_file(file_path, stats)
    except IOError as e:
        print(f"Error writing to file: {e}")


if __name__ == "__main__":
    main()
