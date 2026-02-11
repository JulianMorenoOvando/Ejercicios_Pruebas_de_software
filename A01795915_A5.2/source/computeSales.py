# pylint: disable=invalid-name
"""
This module computes total sales from two JSON files: a price catalogue
and a sales record.
"""

import sys
import json
import time


def load_json_file(file_path):
    """
    Loads a JSON file and handles common errors.
    Returns the loaded data or None if an error occurs.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in - {file_path}")
    except Exception as exc:  # pylint: disable=broad-except
        print(f"An unexpected error occurred while reading {file_path}: {exc}")
    return None


def calculate_total_sales(catalogue_data, sales_data):
    """
    Calculates the total cost for all sales using the price catalogue.
    Returns (total_cost, errors, price_lookup).
    """
    price_lookup = {}

    if isinstance(catalogue_data, list):
        for item in catalogue_data:
            name = item.get("Product") or item.get("title")
            price = item.get("Price") or item.get("price")
            if name is not None and price is not None:
                price_lookup[name] = float(price)

    total_cost = 0.0
    errors = []

    if isinstance(sales_data, list):
        for sale in sales_data:
            product = sale.get("Product")
            quantity = sale.get("Quantity")

            if product is None or quantity is None:
                errors.append(f"Invalid sale record format: {sale}")
                continue

            if product in price_lookup:
                try:
                    total_cost += price_lookup[product] * float(quantity)
                except (ValueError, TypeError):
                    msg = f"Invalid quantity '{product}': {quantity}"
                    errors.append(msg)
            else:
                errors.append(f"Product '{product}' not found in catalogue.")
    else:
        errors.append("Sales data is not a list.")

    return total_cost, errors, price_lookup


def build_report(sales_data, price_lookup, total_cost, elapsed_time, ticket_data):
    """
    Constructs the human-readable sales report as a string.
    """
    report = []
    width = 70
    report.append("-" * width)
    report.append("-" * (width//2) + " TICKET: " + ticket_data + "-" * (width//3))
    report.append("-" * width)
    report.append(f"{'Qtty'!s:<8} {'Product'!s:<40} {'Price'!s:<10}")
    report.append("-" * width)

    if isinstance(sales_data, list):
        for sale in sales_data:
            product = sale.get('Product', 'Unknown')
            price = price_lookup.get(product, 'N/A')
            qty = sale.get('Quantity', 0)
            line = f"{qty!s:<8} {product!s:<40} {price!s:<10}"
            report.append(line)

    report.append("-" * width)
    report.append(f"Total Cost:                       ${total_cost:,.2f}")
    count = len(sales_data) if isinstance(sales_data, list) else 0
    report.append(f"Total Sales Items Processed:      {count}")
    report.append(f"Execution Time:                   {elapsed_time:.6f} secs")
    report.append("-" * width)

    return "\n".join(report)


def save_report(report_text, file_path):
    """
    Saves the report text to the specified file path.
    """
    try:
        with open(file_path, "a", encoding="utf-8") as res_file:
            res_file.write(report_text)
    except Exception as exc:
        print(f"Error saving results to {file_path}: {exc}")


def main():
    """
    Main entry point for the sales calculation script.
    """
    start_time = time.time()

    if len(sys.argv) != 3:
        print("Usage: python computeSales.py catalogue.json sales.json")
        sys.exit(1)

    # Load data
    cat_data = load_json_file(sys.argv[1])
    sales_data = load_json_file(sys.argv[2])
    ticket_data = sys.argv[2].split("/")[-1].split(".")[0]

    if cat_data is None or sales_data is None:
        sys.exit(1)

    # Perform calculations
    total_cost, errors, price_map = calculate_total_sales(cat_data, sales_data)

    # Handle errors
    for error in errors:
        print(f"Data Warning: {error}")

    elapsed = time.time() - start_time

    # Build and save report
    report_text = build_report(sales_data, price_map, total_cost, elapsed, ticket_data)
    print(report_text)
    save_report(report_text, "results/SalesResults.txt")


if __name__ == "__main__":
    main()
