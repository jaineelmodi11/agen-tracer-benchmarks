
FIX = """
Add more test cases.
"""

def vowels_count(s):
    """Write a function vowels_count which takes a string representing
    a word as input and returns the number of vowels in the string.
    Vowels in this case are 'a', 'e', 'i', 'o', 'u'. Here, 'y' is also a
    vowel, but only when it is at the end of the given word.

    Example:
    >>> vowels_count("abcde")
    2
    >>> vowels_count("ACEDY")
    3
    """
    """Write a function vowels_count which takes a string representing
    a word as input and returns the number of vowels in the string.
    Vowels in this case are 'a', 'e', 'i', 'o', 'u'. Here, 'y' is also a
    vowel, but only when it is at the end of the given word.

    Example:
    >>> vowels_count("abcde")
    2
    >>> vowels_count("ACEDY")
    3
    """
    # Check if the input is a string
    if not isinstance(s, str):
    raise ValueError("Input must be a string")

    # Check if the input is empty
    if not s:
    return 0

    # Initialize the count of vowels
    count = 0

    # Iterate through each character in the string
    for char in s:
    # Check if the character is a vowel
    if char.lower() in 'aeiou':
        count += 1

    # Check if the last character is 'y
