import csv

# Print a table row by row
def print_table(table):
    for row in table:
        print(row)

# Read a CSV file and return a nested list
def read_csv_file(file_name):
    table = []
    try:
        with open(file_name, "r", newline='', encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            for row in reader:
                table.append(row)
    except FileNotFoundError:
        print(f"File '{file_name}' not found.")
    except Exception as e:
        print(f"Error reading '{file_name}': {e}")
    return table

# Write a nested list to a CSV file
def write_csv_file(csv_table, file_name):
    try:
        with open(file_name, "w", newline='', encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile, delimiter=",", quoting=csv.QUOTE_MINIMAL)
            for row in csv_table:
                writer.writerow(row)
    except Exception as e:
        print(f"Error writing to '{file_name}': {e}")

# Test reading and writing CSV files
def test_part1_code():
    print("Reading test_case.csv:")
    test_table = read_csv_file("test_case.csv")
    print_table(test_table)
    print()

    print("Writing to test_output.csv:")
    write_csv_file(test_table, "test_output.csv")

    print("Reading test_output.csv:")
    reloaded_table = read_csv_file("test_output.csv")
    print_table(reloaded_table)
    print()

    if test_table == reloaded_table:
        print("Success: tables are the same.")
    else:
        print("Error: tables are different.")

if __name__ == "__main__":
    test_part1_code()
