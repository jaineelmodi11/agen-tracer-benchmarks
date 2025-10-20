

def flip_case(string: str) -> str:
    """ For a given string, flip lowercase characters to uppercase and uppercase to lowercase.
    >>> flip_case('Hello')
    'hELLO'
    """
    return ''.join([char.upper() if char.islower() else char.lower() for char in string])

    # Check function with provided data points
    assert flip_case("Hello") == "hELLO"
    assert flip_case("WorLD") == "wORld"
    assert flip_case("Python3.8") == "pYTHON3.8"

    print("All tests passed.")import re
