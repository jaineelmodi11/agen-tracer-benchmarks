
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
    # Your code here
    return sum(1 for c in s if c.lower() in "aeiou" or (c == 'y' and len(s) > 1))

    # Test cases to verify the correctness of the solution
    print(vowels_count("abcde"))  # Expected output: 2
    print(vowels_count("ACEDY"))  # Expected output: 3
    print(vowels_count("aaaaaaa"))  # Expected output: 4
    print(vowels_count("AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz"))
