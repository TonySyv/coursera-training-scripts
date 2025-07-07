"""
Project for Week 4 of "Python Data Representations".
Find differences in file contents.
"""

IDENTICAL = -1


def singleline_diff(line1, line2):
    """
    Returns the index where the first difference between
    line1 and line2 occurs. Returns IDENTICAL if no difference.
    """
    min_len = min(len(line1), len(line2))
    for idx in range(min_len):
        if line1[idx] != line2[idx]:
            return idx
    if len(line1) != len(line2):
        return min_len
    return IDENTICAL


def singleline_diff_format(line1, line2, idx):
    """
    Formats a string showing the location of the first difference.
    Returns empty string if input lines contain newline/return chars
    or if idx is invalid.
    """
    if '\n' in line1 or '\n' in line2 or '\r' in line1 or '\r' in line2:
        return ""
    if idx < 0 or idx > min(len(line1), len(line2)):
        return ""

    return f"{line1}\n{'=' * idx}^\n{line2}\n"


def multiline_diff(lines1, lines2):
    """
    Returns a tuple (line_num, idx) for the first difference between
    two lists of strings. Returns (IDENTICAL, IDENTICAL) if identical.
    """
    min_lines = min(len(lines1), len(lines2))
    for line_idx in range(min_lines):
        diff_idx = singleline_diff(lines1[line_idx], lines2[line_idx])
        if diff_idx != IDENTICAL:
            return (line_idx, diff_idx)
    if len(lines1) != len(lines2):
        return (min_lines, 0)
    return (IDENTICAL, IDENTICAL)


def get_file_lines(filename):
    """
    Returns a list of lines from the file with newline/return characters removed.
    """
    with open(filename, 'r', encoding='utf-8') as file:
        return [line.rstrip('\n\r') for line in file.readlines()]


def file_diff_format(filename1, filename2):
    """
    Returns a formatted string showing the first difference between two files.
    Returns 'No differences\\n' if files are identical.
    """
    lines1 = get_file_lines(filename1)
    lines2 = get_file_lines(filename2)
    line_num, idx = multiline_diff(lines1, lines2)

    if line_num == IDENTICAL:
        return "No differences\n"

    line1 = lines1[line_num] if line_num < len(lines1) else ""
    line2 = lines2[line_num] if line_num < len(lines2) else ""

    diff = singleline_diff_format(line1, line2, idx)
    return f"Line {line_num}:\n{diff}"


