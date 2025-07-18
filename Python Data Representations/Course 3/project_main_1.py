"""
This module provides utility functions to read and write CSV files
using Python's csv module. It includes functions to:
- Get field names from a CSV file
- Read a CSV file into a list of dictionaries
- Read a CSV file into a nested dictionary
- Write a list of dictionaries back to a CSV file
"""

import csv

def read_csv_fieldnames(filename, separator, quote):
    """
    Inputs:
      filename  - name of CSV file
      separator - character that separates fields
      quote     - character used to optionally quote fields
    Output:
      A list of strings corresponding to the field names in 
      the given CSV file.
    """
    with open(filename, mode='r', newline='', encoding='utf-8') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=separator, quotechar=quote)
        return csvreader.fieldnames


def read_csv_as_list_dict(filename, separator, quote):
    """
    Inputs:
      filename  - name of CSV file
      separator - character that separates fields
      quote     - character used to optionally quote fields
    Output:
      Returns a list of dictionaries where each item in the list
      corresponds to a row in the CSV file. The dictionaries in the
      list map the field names to the field values for that row.
    """
    with open(filename, mode='r', newline='', encoding='utf-8') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=separator, quotechar=quote)
        return list(csvreader)  # Fix: Removed unnecessary comprehension


def read_csv_as_nested_dict(filename, keyfield, separator, quote):
    """
    Inputs:
      filename  - name of CSV file
      keyfield  - field to use as key for rows
      separator - character that separates fields
      quote     - character used to optionally quote fields
    Output:
      Returns a dictionary of dictionaries where the outer dictionary
      maps the value in the key_field to the corresponding row in the
      CSV file. The inner dictionaries map the field names to the
      field values for that row.
    """
    nested_dict = {}
    with open(filename, mode='r', newline='', encoding='utf-8') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=separator, quotechar=quote)
        for row in csvreader:
            nested_dict[row[keyfield]] = row
    return nested_dict


def write_csv_from_list_dict(filename, table, fieldnames, separator, quote):
    """
    Inputs:
      filename   - name of CSV file
      table      - list of dictionaries containing the table to write
      fieldnames - list of strings corresponding to the field names in order
      separator  - character that separates fields
      quote      - character used to optionally quote fields
    Output:
      Writes the table to a CSV file with the name filename, using the
      specified field order and formatting options.
    """
    with open(filename, mode='w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=separator,
                                   quotechar=quote, quoting=csv.QUOTE_NONNUMERIC)
        csvwriter.writeheader()
        for row in table:
            csvwriter.writerow(row)
