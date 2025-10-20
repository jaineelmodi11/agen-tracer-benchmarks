
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

    # Convert all keys to lowercase and compare with their corresponding values
    for key, value in dict.items():
        if isinstance(key, str) and not key.islower() and not value.islower():
            return False

    return True


    # Test cases
    print(check_dict_case({"a":"apple", "b":"banana"}))  # Expected: True
    print(check_dict_case({"a":"apple", "A":"banana", "B":"banana"}))  # Expected: False
    print(check_dict_case({"a":"apple", 8:"banana", "a":"apple"}))  # Expected: False
    print(check_dict_case({"Name":"John", "Age":"36",
