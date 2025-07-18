import csv
import re
from xml.dom import minidom


def get_county_attributes(svg_file_name):
    """
    Parse the SVG file and return a list of tuples.
    Each tuple contains (id, d) attributes for a county.
    """
    # Load and parse the XML file
    dom_tree = minidom.parse(svg_file_name)
    svg = dom_tree.documentElement

    # Get all <path> elements
    paths = svg.getElementsByTagName("path")

    county_attributes = []
    for path in paths:
        if path.hasAttribute("id") and path.hasAttribute("d"):
            county_id = path.getAttribute("id")
            path_data = path.getAttribute("d")
            county_attributes.append((county_id, path_data))

    return county_attributes


def get_boundary_coordinates(boundary_data):
    """
    Extract pairs of floats from path data string, ignoring path commands.
    Return as a list of (x, y) tuples.
    """
    # Regex to find all pairs of floats (handles negative numbers and decimals)
    float_pairs = re.findall(r"(-?\d+\.?\d*),(-?\d+\.?\d*)", boundary_data)
    coordinates = [(float(x), float(y)) for x, y in float_pairs]
    return coordinates


def compute_county_center(boundary_coordinates):
    """
    Compute the center of the polygon given by boundary_coordinates.
    """
    if not boundary_coordinates:
        return (0.0, 0.0)

    x_coords = [point[0] for point in boundary_coordinates]
    y_coords = [point[1] for point in boundary_coordinates]

    center_x = sum(x_coords) / len(x_coords)
    center_y = sum(y_coords) / len(y_coords)

    return (center_x, center_y)


def process_county_attributes(svg_file_name, csv_file_name):
    """
    Parse SVG, compute county centers, and write them to a CSV file.
    """
    counties = get_county_attributes(svg_file_name)

    with open(csv_file_name, mode="w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["FIPS", "Center_X", "Center_Y"])  # Header row

        for county_id, path_data in counties:
            boundary_coords = get_boundary_coordinates(path_data)
            center_x, center_y = compute_county_center(boundary_coords)
            writer.writerow([county_id, center_x, center_y])

    print(f"✅ County centers written to {csv_file_name}")


# -----------------------
# Test the script
# -----------------------
if __name__ == "__main__":
    svg_file = "USA_Counties.svg"  # Replace with your SVG file name
    output_csv = "county_centers.csv"
    
    # Step 1: Test get_county_attributes
    county_data = get_county_attributes(svg_file)
    print(f"Extracted {len(county_data)} counties from SVG.")
    print("First county:", county_data[0])

    # Step 2: Test get_boundary_coordinates
    test_boundary = get_boundary_coordinates(county_data[0][1])
    print("Boundary coordinates sample:", test_boundary[:5])

    # Step 3: Process all counties and write CSV
    process_county_attributes(svg_file, output_csv)
