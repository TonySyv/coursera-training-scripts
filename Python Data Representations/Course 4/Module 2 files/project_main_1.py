"""
GDP Data Plotting Module

Reads GDP data from a CSV file and generates XY plots
showing yearly GDP trends for specified countries using Pygal.
"""
import csv
import pygal

def read_csv_as_nested_dict(filename, keyfield, separator, quote):
    """
    Reads a CSV file and returns a nested dictionary.
    Outer dict keys are values from the column 'keyfield'.
    Inner dicts map fieldnames to field values.

    Inputs:
      filename  - CSV file path
      keyfield  - column name to use as key in outer dict
      separator - delimiter character in CSV
      quote     - quote character in CSV

    Output:
      dict of dicts
    """
    result = {}

    with open(filename, newline='', encoding='utf-8') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=separator, quotechar=quote)
        for row in csvreader:
            key = row[keyfield]
            result[key] = row

    return result


def build_plot_values(gdpinfo, gdpdata):
    """
    Inputs:
      gdpinfo - GDP data information dictionary
      gdpdata - A single country's GDP stored in a dictionary whose
                keys are strings indicating a year and whose values
                are strings indicating the country's corresponding GDP
                for that year.

    Output:
      Returns a list of tuples (year, gdp) suitable for XY plotting.
      Years are integers, GDP values are floats.
      Years with missing GDP data are omitted.
    """
    plot_values = []

    for year in range(gdpinfo['min_year'], gdpinfo['max_year'] + 1):
        year_str = str(year)
        gdp_str = gdpdata.get(year_str, '')
        if gdp_str != '':
            try:
                gdp_val = float(gdp_str)
                plot_values.append((year, gdp_val))
            except ValueError:
                # Skip if GDP data is invalid
                continue

    return plot_values


def build_plot_dict(gdpinfo, country_list):
    """
    Inputs:
      gdpinfo      - GDP data information dictionary
      country_list - List of strings that are country names

    Output:
      Returns a dictionary whose keys are the country names in
      country_list and whose values are lists of XY plot values 
      computed from the CSV file described by gdpinfo.
      If a country is not found, it maps to an empty list.
    """
    gdp_data = read_csv_as_nested_dict(
        gdpinfo['gdpfile'],
        gdpinfo['country_name'],
        gdpinfo['separator'],
        gdpinfo['quote']
    )

    result = {}

    for country in country_list:
        if country in gdp_data:
            result[country] = build_plot_values(gdpinfo, gdp_data[country])
        else:
            result[country] = []

    return result


def render_xy_plot(gdpinfo, country_list, plot_file):
    """
    Inputs:
      gdpinfo      - GDP data information dictionary
      country_list - List of strings that are country names
      plot_file    - String that is the output plot file name

    Output:
      Returns None. Creates an SVG plot saved to plot_file.
    """
    # Build the data dictionary for plotting
    plot_dict = build_plot_dict(gdpinfo, country_list)

    # Create a pygal XY plot
    xy_chart = pygal.XY(
        title='GDP Over Time',
        x_title='Year',
        y_title='GDP (current US$)',
        show_legend=True,
        legend_at_bottom=True,
        show_dots=False,
        stroke=True,
        x_label_rotation=20,
        truncate_label=-1
    )

    # Add data series to the plot
    for country, values in plot_dict.items():
        xy_chart.add(country, values)

    # Save the plot to the specified file
    xy_chart.render_to_file(plot_file)


# Example usage:
if __name__ == '__main__':
    gdp_info = {
        "gdpfile": "isp_gdp.csv",        # Name of the GDP CSV file
        "separator": ",",                # Separator character in CSV file
        "quote": '"',                    # Quote character in CSV file
        "min_year": 1960,                # Oldest year of GDP data in CSV file
        "max_year": 2015,                # Latest year of GDP data in CSV file
        "country_name": "Country Name",  # Country name field name
        "country_code": "Country Code"   # Country code field name (not used here)
    }

    countries = ["China", "United States", "United Kingdom"]
    output_file = "gdp_plot.svg"

    print("🔄 Generating GDP plot...")
    render_xy_plot(gdp_info, countries, output_file)
    print(f"✅ Plot saved to {output_file}")
