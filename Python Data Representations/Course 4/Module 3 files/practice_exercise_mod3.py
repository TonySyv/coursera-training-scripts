import csv

def read_csv_file(filename):
    """
    Reads a CSV file without assuming a header row.
    Returns a list of rows, each a list of strings.
    """
    with open(filename, newline='') as f:
        reader = csv.reader(f)
        return list(reader)

def make_dict(table, key_col):
    """
    Creates a dictionary keyed by the value at column key_col.
    Each value is the row with the key column removed.
    """
    result = {}
    for row in table:
        key = row[key_col]
        # value is the rest of the row except the key column
        value = row[:key_col] + row[key_col+1:]
        result[key] = value
    return result

def merge_csv_files(cancer_csv_file, center_csv_file, joined_csv_file):
    """
    Reads cancer risk data and county center data,
    merges by FIPS code (column index 2),
    writes the merged data to joined_csv_file.
    Also prints FIPS codes missing in one dataset but present in the other.
    """
    # Read CSV files (no headers)
    cancer_data = read_csv_file(cancer_csv_file)
    center_data = read_csv_file(center_csv_file)

    # Create dictionaries keyed by FIPS code (index 2)
    cancer_dict = make_dict(cancer_data, 2)
    center_dict = make_dict(center_data, 2)

    # Prepare output header (you can add or adjust as needed)
    header = [
        "State", "County name", "FIPS code", "Population", "Cancer risk",
        "Horizontal coordinate", "Vertical coordinate"
    ]

    # Open output CSV to write
    with open(joined_csv_file, 'w', newline='') as f_out:
        writer = csv.writer(f_out)
        writer.writerow(header)

        # Track how many matches and mismatches
        matched = 0
        missing_in_center = []
        missing_in_cancer = []

        # Merge rows where FIPS exists in both datasets
        for fips, cancer_values in cancer_dict.items():
            if fips in center_dict:
                center_values = center_dict[fips]
                # Compose merged row:
                # cancer_values = [State, County, Population, Cancer risk, ... ?]
                # We expect cancer_values order:
                # [State, County name, Population, Cancer risk, ...] but actually
                # cancer_values came from removing FIPS at index 2, so indexes shift.

                # From your sample, cancer_values = [State, County name, Population, Cancer risk, ...]
                # But from your line example, cancer_data row is:
                # [0] State, [1] County, [2] FIPS, [3] Population, [4] Cancer risk, [5] Hor coord, [6] Vert coord
                # You removed index 2 (FIPS), so cancer_values = [State, County, Population, Cancer risk, Hor coord, Vert coord?]
                # But since your cancer CSV doesn't have center coords, assume cancer_values only up to Cancer risk (indexes 0-3)
                # So, cancer_values: [State, County name, Population, Cancer risk, ...?]

                # center_values: after removing FIPS (index 2), should be: [Hor coord, Vert coord]

                # To be safe, let's print lengths (optional debugging)
                # print(len(cancer_values), len(center_values))

                # We'll select only required columns from cancer_values: State, County name, Population, Cancer risk
                # Then append center coords from center_values (which should be two floats)

                merged_row = [
                    cancer_values[0],  # State
                    cancer_values[1],  # County name
                    fips,             # FIPS code (key)
                    cancer_values[2],  # Population
                    cancer_values[3],  # Cancer risk
                    center_values[0],  # Horizontal coordinate
                    center_values[1],  # Vertical coordinate
                ]
                writer.writerow(merged_row)
                matched += 1
            else:
                missing_in_center.append(fips)

        # Check for FIPS codes in center_dict not in cancer_dict
        for fips in center_dict:
            if fips not in cancer_dict:
                missing_in_cancer.append(fips)

    # Print summary of anomalies
    print(f"Total cancer entries: {len(cancer_dict)}")
    print(f"Total center entries: {len(center_dict)}")
    print(f"Matched entries: {matched}")
    print(f"FIPS codes missing in center data: {len(missing_in_center)}")
    print(f"FIPS codes missing in cancer data: {len(missing_in_cancer)}")

    # Optionally, print some missing codes for inspection
    if missing_in_center:
        print("Sample FIPS missing in center data:", missing_in_center[:10])
    if missing_in_cancer:
        print("Sample FIPS missing in cancer data:", missing_in_cancer[:10])

if __name__ == "__main__":
    cancer_csv_file = "cancer_risk_trimmed_solution.csv"
    center_csv_file = "USA_Counties_with_FIPS_and_centers.csv"
    joined_csv_file = "cancer_risk_joined_solution.csv"

    merge_csv_files(cancer_csv_file, center_csv_file, joined_csv_file)
