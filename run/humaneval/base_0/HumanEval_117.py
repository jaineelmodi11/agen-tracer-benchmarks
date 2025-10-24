
def select_words(s, n):
    """Given a string s and a natural number n, you have been tasked to implement 
    a function that returns a list of all words from string s that contain exactly 
    n consonants, in order these words appear in the string s.
    If the string s is empty then the function should return an empty list.
    Note: you may assume the input string contains only letters and spaces.
    Examples:
    select_words("Mary had a little lamb", 4) ==> ["little"]
    select_words("Mary had a little lamb", 3) ==> ["Mary", "lamb"]
    select_words("simple white space", 2) ==> []
    select_words("Hello world", 4) ==> ["world"]
    select_words("Uncle sam", 3) ==> ["Uncle"]
    """
    # Initialize an empty list to store the words
    result = []

    # Iterate through each character in the string
    for char in s:
    # Check if the character is a consonant
    if char.lower() in 'bcdfghjklmnpqrstvwxyz':
        # If the count of consonants matches n, add the word to the result
        if len(result) == n:
            result.append(char)
        # If the count of consonants does not match n, skip the current character
        elif len(result) < n:
            continue

    # Return the list of words that contain exactly n consonants
    return result
