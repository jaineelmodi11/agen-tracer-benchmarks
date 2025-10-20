
def check_dict_case(dict):
    """
    Given a dictionary, return True if all keys are strings in lower 
    case or all keys are strings in upper case, else return False.
    The function should return False is the given dictionary is empty.
    Examples:
    check_dict_case({"a":"apple", "b":"banana"}) should return True.
    check_dict_case({"a":"apple", "A":"banana", "B":"banana"}) should return False.
    check_dict_case({"a":"apple", 8:"banana", "a":"apple"}) should return False.
    check_dict_case({"Name":"John", "Age":"36", "City":"Houston"}) should return False.
    check_dict_case({"STATE":"NC", "ZIP":"12345" }) should return True.
    """
    # Check if the dictionary is empty
    if not dict:
        return False

    # Check if all keys are strings and in lower case
    for key in dict.keys():
        if not isinstance(key, str) or len(key) == 0:
            return False
        elif key.isupper() or key.islower():
            continue
        else:
            return False

    return True

    # Example usage
    print(check_dict_case({"a":"apple", "b":"banana"}))  # Should return True
    print(check_dict_case({"a":"apple", "A":"banana", "B":"banana"}))  # Should return False
    print(check_dict_case({"a":"apple", 8:"banana", "a":"apple"}))  # Should return False
