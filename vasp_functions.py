"""
Set of functions designed to read and extract information from VASP output files.
@Author: Marco A. Villena
@email: mavillenas@hotmail.com
@Date: 2022-2023
"""

# ---- Libraries ----
import os


def f_total_atoms(in_filepath, in_line_number=7):
    """
    Read the number of atoms from POSCAR file and return the total of atoms number.

    Args:
        in_filepath (str): Path of the POSCAR file.
        in_line_number (int): Line number where the number of atoms is in the POSCAR file. (Default: 7)

    Returns: Return the total number of atoms. If this paramente is not found, it returns 0.

    """

    fullpath = os.path.join(in_filepath, 'POSCAR')

    with open(fullpath, "r") as f:
        lines = f.readlines()
        line = lines[in_line_number - 1]
        numbers = line.split()

        total = 0
        for item in line.split():
            try:
                total += int(item)
            except ValueError:
                pass

        return total


def f_postions_forces(in_filepath, in_total_lines, in_lines_ignored, in_position='last', in_keyword='TOTAL-FORCE'):
    """
    Return the position and forces of all atoms. This information is extracted from the last or first TOTAL-FORCE report in the OUTCAR file.

    Args:
        in_filepath (str): Path of the OUTCAR file.
        in_total_lines (int): Total lines that must be saved after the keyword
        in_lines_ignored (int): Total lines ignored just after the keyword line
        in_position (str): Identify if it looks for the first or the last time that the keyword appears (Default: last)
        in_keyword (str): Keyword that determine the begining of the lines of interest (Default: TOTAL-FORCE)

    Returns: Return the list with all positions and forces of all saved lines. If the keyword is not found, it returns -1.

    """

    fullpath = os.path.join(in_filepath, 'OUTCAR')
    # Open de file
    with open(fullpath, 'r') as archivo:
        lines = archivo.readlines()

    # Search for the last line that contains the keyword
    keyword_index = None
    if in_position == 'last':
        for index in range(len(lines) - 1, -1, -1):
            if in_keyword in lines[index]:
                keyword_index = index + in_lines_ignored
                break
    elif in_position == 'first':
        for index in range(len(lines)):
            if in_keyword in lines[index]:
                keyword_index = index + in_lines_ignored
                break
    else:
        return -2  # ERROR: The position is not correctly defined (first or last)

    # Create an empty list to store the following lines
    lineas_posteriores = []

    if keyword_index is not None:
        # Copy the lines following the last line that contains the keyword
        for i in range(keyword_index + 1, min(keyword_index + in_total_lines + 1, len(lines))):
            lineas_posteriores.append(lines[i])

        # Create an empty list to store the numeric values_list of the lines
        values_list = []

        # Iterate through the following lines
        for item in lineas_posteriores:
            # Split each line into its numeric values_list
            item_values = item.strip().split()
            # Convert each value to a number and add it to the list of values_list
            values_list.append([float(element) for element in item_values])

        return values_list
    else:
        return -1  # ERROR: Keyword not found


def f_find_string_in_file(in_file_path, in_string):
    """
    This function creates a list with all lines from a text file that contain the <in_string>.

    Args:
        in_file_path (str): Path of the file to scan.
        in_string (str): String to searchc in the text file.

    Returns:
        found_lines (list): List with all lines that contain the string.
    """

    found_lines = []

    with open(in_file_path, 'r') as file:
        for line in file:
            if in_string in line:
                found_lines.append(line.strip())

    return found_lines
