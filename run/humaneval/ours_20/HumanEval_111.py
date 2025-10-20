
def histogram(test):
    """Given a string representing a space separated lowercase letters, return a dictionary
    of the letter with the most repetition and containing the corresponding count.
    If several letters have the same occurrence, return all of them.
    
    Example:
    histogram('a b c') == {'a': 1, 'b': 1, 'c': 1}
    histogram('a b b a') == {'a': 2, 'b': 2}
    histogram('a b c a b') == {'a': 2, 'b': 2}
    histogram('b b b b a') == {'b': 4}
    histogram('') == {}

    """
    from collections import Counter

    # Convert the input string into a list of characters
    chars = list(test)

    # Use Counter to get the frequency of each character
    char_count = Counter(chars)

    # Find the maximum frequency
    max_freq = max(char_count.values())

    # Filter the characters that have the maximum frequency
    result = {char: freq for char, freq in char_count.items() if freq == max_freq}

    return result
