"""
Project: Plotting GDP Data on a World Map - Part 1

This script reads GDP data from a CSV file and generates a world map plot
using Pygal, showing the log of GDP for countries in a specific year.
"""

import csv
import math
import pygal


def read_csv_as_nested_dict(filename, keyfield, separator, quote):
    """
    Read a CSV file and return a nested dictionary.

    filename  - name of the CSV file
    keyfield  - field to use as the key for the outer dictionary
    separator - character that separates fields
    quote     - character used to optionally quote fields

    Returns: A dictionary of dictionaries where the outer dictionary
    maps the value in the key_field to the corresponding row in the CSV file.
    """
    result = {}
    with open(filename, newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=separator, quotechar=quote)
        for row in reader:
            result[row[keyfield]] = row
    return result


def reconcile_countries_by_name(plot_countries, gdp_countries):
    """
    Reconcile country names between Pygal and GDP data.

    plot_countries - dictionary of Pygal country codes to country names
    gdp_countries  - dictionary of country names in GDP data

    Returns: A tuple containing:
      - A dictionary mapping Pygal country codes to country names
        found in GDP data.
      - A set of Pygal country codes not found in GDP data.
    """
    reconciled_dict = {}
    missing_countries = set()

    for code, name in plot_countries.items():
        if name in gdp_countries:
            reconciled_dict[code] = name
        else:
            missing_countries.add(code)

    return reconciled_dict, missing_countries


def build_map_dict_by_name(gdp_info, plot_countries, year):
    """
    Build a mapping of Pygal country codes to log10 GDP values for a given year.

    gdp_info       - GDP information dictionary
    plot_countries - Pygal country codes to country names
    year           - year to extract GDP data for (as a string)

    Returns: A tuple containing:
      - A dictionary mapping Pygal country codes to log10 GDP values
      - A set of Pygal country codes not found in the GDP data
      - A set of Pygal country codes with no GDP data for the specified year
    """
    gdp_data = read_csv_as_nested_dict(
        gdp_info["gdpfile"],
        gdp_info["country_name"],
        gdp_info["separator"],
        gdp_info["quote"]
    )

    reconciled, missing_countries = reconcile_countries_by_name(
        plot_countries, gdp_data
    )

    gdp_map = {}
    no_gdp_countries = set()

    for code, name in reconciled.items():
        gdp_entry = gdp_data[name]
        gdp_value = gdp_entry.get(year, "")
        if gdp_value != "":
            try:
                gdp_float = float(gdp_value)
                if gdp_float > 0:
                    gdp_map[code] = math.log10(gdp_float)
                else:
                    no_gdp_countries.add(code)
            except ValueError:
                no_gdp_countries.add(code)
        else:
            no_gdp_countries.add(code)

    return gdp_map, missing_countries, no_gdp_countries


def render_world_map(gdp_info, plot_countries, year, map_file):
    """
    Render a world map showing GDP data.

    gdp_info       - GDP information dictionary
    plot_countries - Pygal country codes to country names
    year           - year for GDP data (string)
    map_file       - filename for the output SVG file
    """
    gdp_map, missing_countries, no_gdp_countries = build_map_dict_by_name(
        gdp_info, plot_countries, year
    )

    worldmap = pygal.maps.world.World()
    worldmap.title = f"Global GDP in {year} (log scale)"
    worldmap.add("GDP (log)", gdp_map)
    worldmap.add("Missing from GDP data", missing_countries)
    worldmap.add("No GDP for this year", no_gdp_countries)

    worldmap.render_to_file(map_file)
    print(f"World map saved to {map_file}")


# Example GDP info
gdpinfo = {
    "gdpfile": "isp_gdp.csv",
    "separator": ",",
    "quote": '"',
    "min_year": 1960,
    "max_year": 2015,
    "country_name": "Country Name",
    "country_code": "Country Code"
}


# Example usage
if __name__ == "__main__":
    render_world_map(gdpinfo, pygal.maps.world.COUNTRIES, "2000", "world_gdp_2000.svg")
