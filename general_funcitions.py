"""
Set of general purpose functions.
@Author: Marco A. Villena
@email: mavillenas@hotmail.com
@Date: 2022-2023
"""

# ---- Libraries ----
import os


def find_folders_with_string(in_path, in_substring):
    """
    FIND_FOLDERS_WITH_STRING generates a list with all folders that contains a giving string in its name

    Args:
        in_path (str): Path of the work folder
        in_substring (str): String that the folder name must contain

    Returns: The list of found folders

    """

    folder_list = []
    for folder_name in os.listdir(in_path):
        if os.path.isdir(os.path.join(in_path, folder_name)) and in_substring in folder_name:
            folder_list.append(folder_name)
    return folder_list

