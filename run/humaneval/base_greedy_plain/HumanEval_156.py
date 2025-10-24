
def int_to_mini_roman(number):
    """
    Given a positive integer, obtain its roman numeral equivalent as a string,
    and return it in lowercase.
    Restrictions: 1 <= num <= 1000

    Examples:
    >>> int_to_mini_roman(19) == 'xix'
    >>> int_to_mini_roman(152) == 'clii'
    >>> int_to_mini_roman(426) == 'cdxxvi'
    """
    # Mapping of integers to their roman numeral counterparts
    roman_map = {
        1000: 'm', 900: 'cm', 500: 'd', 400: 'cd',
        100: 'c', 90: 'xc', 50: 'l', 40: 'xl',
        10: 'x', 9: 'ix', 5: 'v', 4: 'iv', 1: 'i'
    }

    # Initialize the result string
    result = ''

    # Iterate over the mapping in reverse order to handle the largest numbers first
    for value, numeral in sorted(roman_map.items(), reverse=True):
        while number >= value:
            result += numeral
            number -= value

    return result

    # Check function to verify the correctness of the solution
