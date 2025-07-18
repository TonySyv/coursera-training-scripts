"""
Practice Project: Processing Cancer-Risk Data

This script provides functions for reading and writing CSV files,
selecting specific columns from 2D tables (nested lists),
and sorting tables by a numerical column in descending order.

Functions:
- read_csv_file(file_name)
- write_csv_file(csv_table, file_name)
- select_columns(my_table, col_indices)
- sort_by_column(my_table, col_idx)
- print_table(table)
- test_part2_code()
"""

import csv


def read_csv_file(file_name):
    """
    Given a file path specified as the string file_name,
    load the associated CSV file and return a nested list
    whose entries are the fields in the CSV file.
    Each entry in the returned table is of type str.
    """
    with open(file_name, mode="r", newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        table = [row for row in csvreader]
    return table


def write_csv_file(csv_table, file_name):
    """
    Given a nested list csv_table and a file path specified
    as the string file_name, write entries in the nested list
    as the fields of a comma-separated CSV file with the specified path.
    """
    with open(file_name, mode="w", newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        for row in csv_table:
            csvwriter.writerow(row)


def select_columns(my_table, col_indices):
    """
    Given a nested list my_table and a list of integers col_indices,
    return a new 2D table (as a nested list) consisting of only
    those items in the specified columns.
    """
    new_table = []
    for row in my_table:
        new_row = [row[col_idx] for col_idx in col_indices]
        new_table.append(new_row)
    return new_table


def sort_by_column(my_table, col_idx):
    """
    Given a nested list my_table and an integer col_idx,
    mutate my_table by sorting its rows such that items
    in the column specified by col_idx are in descending order
    when interpreted as numbers.
    """
    header = my_table[0]
    data = my_table[1:]
    data.sort(key=lambda row: float(row[col_idx]), reverse=True)
    my_table[:] = [header] + data


def print_table(table):
    """
    Print a 2D table in a nicely formatted way.
    """
    for row in table:
        print(", ".join(row))


def test_part2_code():
    """
    Test select_columns and sort_by_column using a small test file,
    then process the cancer-risk data.
    """
    print("Testing with test_case.csv...")
    test_table = read_csv_file("test_case.csv")
    print("Original table:")
    print_table(test_table)

    # Test select_columns
    selected = select_columns(test_table, [0, 2])
    print("\nSelected columns (0 and 2):")
    print_table(selected)

    # Test sort_by_column
    print("\nSorting by column 1 (descending):")
    sort_by_column(test_table, 1)
    print_table(test_table)

    # Process cancer-risk data
    print("\nProcessing cancer_risk.csv...")
    cancer_table = read_csv_file("cancer_risk.csv")
    # Select columns: A, B, C, E, L (0-based indices: 0, 1, 2, 4, 11)
    trimmed_table = select_columns(cancer_table, [0, 1, 2, 4, 11])
    write_csv_file(trimmed_table, "cancer_risk_trimmed.csv")
    print("Trimmed data written to cancer_risk_trimmed.csv.")


# Run tests when the script is executed directly
if __name__ == "__main__":
    test_part2_code()
