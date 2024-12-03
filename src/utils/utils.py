

def merge_dictionaries(dictionary1, dictionary2):
    my_dict = dictionary1.copy()
    for key, value in dictionary2.items():
        if key in my_dict and isinstance(my_dict[key], dict) and isinstance(value, dict):
            my_dict[key] = merge_dictionaries(my_dict[key], value)
        else:
            my_dict[key] = value
    return my_dict