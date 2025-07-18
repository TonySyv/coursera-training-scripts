"""
Project: Analyzing Baseball Data

This script processes historical MLB batting data to compute
top players based on various batting statistics.
"""

import csv


###########################################################
# Provided utility functions (DO NOT MODIFY)
###########################################################

def read_csv_as_list_dict(filename, separator, quote):
    """
    Read the given CSV file and return a list of dictionaries.

    Each dictionary maps field names to field values for that row.
    """
    with open(filename, newline='', encoding='utf-8') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=separator, quotechar=quote)
        return list(csvreader)


def read_csv_as_nested_dict(filename, keyfield, separator, quote):
    """
    Read the given CSV file and return a nested dictionary.

    The outer dictionary maps the value in the key_field to the corresponding row.
    """
    result = {}
    with open(filename, newline='', encoding='utf-8') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=separator, quotechar=quote)
        for row in csvreader:
            result[row[keyfield]] = row
    return result


###########################################################
# Provided batting statistic functions
###########################################################

def batting_average(info, batting_stats):
    """
    Compute the batting average for a player.
    """
    hits = int(batting_stats.get(info["hits"], 0))
    at_bats = int(batting_stats.get(info["atbats"], 0))
    if at_bats >= 500:
        return hits / at_bats
    else:
        return 0.0


def onbase_percentage(info, batting_stats):
    """
    Compute the on-base percentage for a player.
    """
    hits = int(batting_stats.get(info["hits"], 0))
    walks = int(batting_stats.get(info["walks"], 0))
    at_bats = int(batting_stats.get(info["atbats"], 0))
    if at_bats + walks >= 500:
        return (hits + walks) / (at_bats + walks)
    else:
        return 0.0


def slugging_percentage(info, batting_stats):
    """
    Compute the slugging percentage for a player.
    """
    hits = int(batting_stats.get(info["hits"], 0))
    doubles = int(batting_stats.get(info["doubles"], 0))
    triples = int(batting_stats.get(info["triples"], 0))
    homeruns = int(batting_stats.get(info["homeruns"], 0))
    singles = hits - doubles - triples - homeruns
    at_bats = int(batting_stats.get(info["atbats"], 0))
    if at_bats >= 500:
        total_bases = singles + 2 * doubles + 3 * triples + 4 * homeruns
        return total_bases / at_bats
    else:
        return 0.0


###########################################################
# Part 1: Compute top batting stats by year
###########################################################

def filter_by_year(statistics, year, yearid):
    """
    Filter batting statistics dictionaries by year.
    """
    return [stat for stat in statistics if int(stat[yearid]) == year]


def top_player_ids(info, statistics, formula, numplayers):
    """
    Compute top players with the given formula and return their IDs and stats.
    """
    player_stats = []
    for stat in statistics:
        value = formula(info, stat)
        player_stats.append((stat[info["playerid"]], value))
    # Sort by stat descending
    player_stats.sort(key=lambda x: x[1], reverse=True)
    return player_stats[:numplayers]


def lookup_player_names(info, top_ids_and_stats):
    """
    Return formatted list of top players with names and stats.
    """
    master_dict = read_csv_as_nested_dict(
        info["masterfile"],
        info["playerid"],
        info["separator"],
        info["quote"]
    )
    result = []
    for player_id, stat in top_ids_and_stats:
        first_name = master_dict[player_id][info["firstname"]]
        last_name = master_dict[player_id][info["lastname"]]
        result.append(f"{stat:.3f} --- {first_name} {last_name}")
    return result


def compute_top_stats_year(info, formula, numplayers, year):
    """
    Compute top players for a specific year.
    """
    batting_stats = read_csv_as_list_dict(
        info["battingfile"],
        info["separator"],
        info["quote"]
    )
    stats_year = filter_by_year(batting_stats, year, info["yearid"])
    top_players = top_player_ids(info, stats_year, formula, numplayers)
    return lookup_player_names(info, top_players)


###########################################################
# Part 2: Compute top batting stats by career
###########################################################

def aggregate_by_player_id(statistics, playerid, fields):
    """
    Aggregate yearly batting stats into career stats for each player.
    """
    aggregated = {}
    for stat in statistics:
        pid = stat[playerid]
        if pid not in aggregated:
            aggregated[pid] = {playerid: pid}
            for field in fields:
                aggregated[pid][field] = int(stat.get(field, 0))
        else:
            for field in fields:
                aggregated[pid][field] += int(stat.get(field, 0))
    return aggregated


def compute_top_stats_career(info, formula, numplayers):
    """
    Compute top players over their entire career.
    """
    batting_stats = read_csv_as_list_dict(
        info["battingfile"],
        info["separator"],
        info["quote"]
    )
    career_stats = aggregate_by_player_id(
        batting_stats,
        info["playerid"],
        info["battingfields"]
    )
    # Convert aggregated dict to list
    career_stats_list = list(career_stats.values())
    top_players = top_player_ids(info, career_stats_list, formula, numplayers)
    return lookup_player_names(info, top_players)


###########################################################
# Example baseball data info dictionary
###########################################################

baseballdatainfo = {
    "masterfile": "Master_2016.csv",
    "battingfile": "Batting_2016.csv",
    "separator": ",",
    "quote": '"',
    "playerid": "playerID",
    "firstname": "nameFirst",
    "lastname": "nameLast",
    "yearid": "yearID",
    "atbats": "AB",
    "hits": "H",
    "doubles": "2B",
    "triples": "3B",
    "homeruns": "HR",
    "walks": "BB",
    "battingfields": ["AB", "H", "2B", "3B", "HR", "BB"]
}


###########################################################
# Test function
###########################################################

def test_baseball_statistics():
    """
    Run a series of tests on the baseball statistics functions.
    """
    print("Top 5 Batting Average in 2010:")
    print("\n".join(compute_top_stats_year(baseballdatainfo, batting_average, 5, 2010)))

    print("\nTop 5 On-Base Percentage in 2010:")
    print("\n".join(compute_top_stats_year(baseballdatainfo, onbase_percentage, 5, 2010)))

    print("\nTop 5 Slugging Percentage in 2010:")
    print("\n".join(compute_top_stats_year(baseballdatainfo, slugging_percentage, 5, 2010)))

    print("\nTop 10 Batting Average Career:")
    print("\n".join(compute_top_stats_career(baseballdatainfo, batting_average, 10)))


###########################################################
# Main program (only runs tests when executed directly)
###########################################################

if __name__ == "__main__":
    test_baseball_statistics()
