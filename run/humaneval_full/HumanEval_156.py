
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
    # Mapping of digits to their Roman numeral counterparts
    digit_to_roman = {
    1: 'i', 4: 'iv', 5: 'v', 9: 'ix',
    2: 'ii', 3: 'iii', 4: 'iv', 6: 'vi',
    7: 'vii', 8: 'viii', 9: 'ix'
    }

    # Convert the number to a string, ensuring it
