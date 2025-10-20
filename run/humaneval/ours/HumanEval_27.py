

def flip_case(string: str) -> str:
    """ For a given string, flip lowercase characters to uppercase and uppercase to lowercase.
    >>> flip_case('Hello')
    'hELLO'
    """
        result.append(char.upper())
    elif char.isupper():
        result.append(char.lower())
    else:
        result.append(char)
    return ''.join(result)
