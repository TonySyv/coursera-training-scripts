"""
Module to process and plot World Bank GDP data on a Pygal world map,
reconciling country codes between datasets.
"""

import csv
import math
import pygal


def read_csv_as_list_dict(filename, separator, quote):
    """
    Reads a CSV file and returns a list of dictionaries,
    where each dictionary corresponds to a row with header keys.
    """
    with open(filename, newline='', encoding='utf-8') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=separator, quotechar=quote)
        return list(csvreader)


def build_country_code_converter(country_code_info):
    """
    Inputs:
      country_code_info - A dictionary with keys specifying the country code CSV
                         file and relevant column names for plot and data codes.

    Output:
      A dictionary mapping plot country codes (e.g. 'us') to World Bank country codes (e.g. 'USA').
      Case is preserved exactly as found in the CSV.
    """
    code_list = read_csv_as_list_dict(
        country_code_info['codefile'],
        country_code_info['separator'],
        country_code_info['quote']
    )
    converter = {}
    for entry in code_list:
        plot_code = entry[country_code_info['plot_codes']]
        data_code = entry[country_code_info['data_codes']]
        converter[plot_code] = data_code
    return converter


def reconcile_countries_by_code(country_code_info, plot_countries_dict, gdp_countries_dict):
    """
    Inputs:
      country_code_info  - Country code information dictionary
      plot_countries_dict - Dictionary mapping plot library country codes to country names
      gdp_countries_dict  - Dictionary mapping GDP country codes to data (values ignored)

    Outputs:
      Tuple of (dict, set):
      - dict mapping plot country codes to GDP country codes (matching by code equivalency)
      - set of plot country codes not found in GDP data
    """
    converter = build_country_code_converter(country_code_info)

    # Case-insensitive lookup dictionaries
    converter_upper = {k.upper(): v for k, v in converter.items()}
    gdp_codes_upper = {k.upper(): k for k in gdp_countries_dict.keys()}

    reconciled_dict = {}
    missing_set = set()

    for plot_code in plot_countries_dict.keys():
        plot_code_upper = plot_code.upper()
        if plot_code_upper in converter_upper:
            gdp_code = converter_upper[plot_code_upper]
            if gdp_code.upper() in gdp_codes_upper:
                real_gdp_code = gdp_codes_upper[gdp_code.upper()]
                reconciled_dict[plot_code] = real_gdp_code
            else:
                missing_set.add(plot_code)
        else:
            missing_set.add(plot_code)

    return reconciled_dict, missing_set


def load_gdp_data(gdp_info):
    """
    Helper function to load GDP data from file into dictionary keyed by country code.
    """
    rows = read_csv_as_list_dict(
        gdp_info['gdpfile'],
        gdp_info['separator'],
        gdp_info['quote']
    )
    gdp_dict = {}
    for row in rows:
        country_code = row[gdp_info['country_code']].strip()
        gdp_dict[country_code] = row
    return gdp_dict


def build_map_dict_by_code(gdpinfo_param, codeinfo_param, plot_countries_param, year_param):
    """
    Creates a mapping from plot country codes to the log base 10 of GDP for a specified year.

    Inputs:
      gdpinfo_param        - Dictionary containing GDP data file info.
      codeinfo_param       - Dictionary containing country code mapping file info.
      plot_countries_param - Dictionary mapping plot library country codes to country names.
      year_param           - String representing the year to map GDP data for.

    Outputs:
      A tuple containing:
        - A dictionary mapping plot country codes to the log10 of GDP for the specified year.
        - A set of country codes from plot_countries_param not found in the GDP data.
        - A set of country codes found in the GDP data but missing GDP info for the specified year.
    """
    gdp_countries = load_gdp_data(gdpinfo_param)
    reconciled, missing_countries = reconcile_countries_by_code(
        codeinfo_param, plot_countries_param, gdp_countries
    )

    no_data_countries = set()
    map_dict = {}

    for plot_code, gdp_code in reconciled.items():
        gdp_row = gdp_countries.get(gdp_code)
        if gdp_row is None:
            no_data_countries.add(plot_code)
            continue

        gdp_value_str = gdp_row.get(year_param, "")
        if not gdp_value_str:
            no_data_countries.add(plot_code)
            continue

        try:
            gdp_value = float(gdp_value_str)
            if gdp_value > 0:
                map_dict[plot_code] = math.log10(gdp_value)
            else:
                no_data_countries.add(plot_code)
        except ValueError:
            no_data_countries.add(plot_code)

    return map_dict, missing_countries, no_data_countries


def render_world_map(gdp_info, country_code_info, plot_countries_dict, year_str, output_filename):
    """
    Inputs:
      gdp_info            - GDP info dictionary
      country_code_info   - Country code info dictionary
      plot_countries_dict - Dictionary mapping plot library country codes to country names
      year_str            - Year string
      output_filename     - Output SVG file name

    Output:
      Writes an SVG file of the world map with GDP data plotted.
    """
    gdp_map, missing_countries, no_gdp_countries = build_map_dict_by_code(
        gdp_info, country_code_info, plot_countries_dict, year_str
    )

    worldmap_chart = pygal.maps.world.World()
    worldmap_chart.title = f'World GDP for {year_str} (log scale)'

    # Countries with GDP data
    worldmap_chart.add(f'GDP for {year_str}', gdp_map)
    # Countries missing from GDP data entirely
    worldmap_chart.add('Missing from GDP data', list(missing_countries))
    # Countries with no GDP data for this year
    worldmap_chart.add(f'No GDP data for {year_str}', list(no_gdp_countries))

    worldmap_chart.render_to_file(output_filename)


if __name__ == "__main__":
    gdpinfo = {
        "gdpfile": "isp_gdp.csv",
        "separator": ",",
        "quote": '"',
        "min_year": "1960",
        "max_year": "2010",
        "country_name": "Country Name",
        "country_code": "Country Code"
    }
    codeinfo = {
        "codefile": "isp_country_codes.csv",
        "separator": ",",
        "quote": '"',
        "plot_codes": "ISO3166-1-Alpha-2",
        "data_codes": "ISO3166-1-Alpha-3"
    }
    plot_countries = pygal.maps.world.COUNTRIES
    year = "2000"
    render_world_map(gdpinfo, codeinfo, plot_countries, year, "isp_gdp_world_code_2000.svg")
