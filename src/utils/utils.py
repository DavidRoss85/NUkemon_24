import copy
import os


def merge_dictionaries(dictionary1, dictionary2):
    """
    Recursive tool for merging nested dictionaries while preserving structure
    """
    my_dict1 =dictionary1.copy()
    my_dict2 =dictionary2.copy()

    for key, value in my_dict2.items():
        if key in my_dict1 and isinstance(my_dict1[key], dict) and isinstance(value, dict):
            my_dict1[key] = merge_dictionaries(my_dict1[key], value)
        else:
            my_dict1[key] = value
    return my_dict1


def count_lines_in_project(directory):
    """
    Tool to count lines of code across project
    :param directory: root directory
    :return: Integer (Total number of lines across all files)
    """
    total_lines=0
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                file_path= os.path.join(root,file)
                with open(file_path, 'r',encoding='utf-8') as f:
                    lines = f.readlines()
                    total_lines += len(lines)

    return total_lines