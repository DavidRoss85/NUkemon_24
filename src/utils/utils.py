import os


def merge_dictionaries(dictionary1, dictionary2):
    """
    Recursive tool for merging nested dictionaries while preserving structure
    """
    my_dict = dictionary1.copy()
    for key, value in dictionary2.items():
        if key in my_dict and isinstance(my_dict[key], dict) and isinstance(value, dict):
            my_dict[key] = merge_dictionaries(my_dict[key], value)
        else:
            my_dict[key] = value
    return my_dict


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