
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
    # Count the frequency of each character in the test string
    char_count = collections.Counter(test)

    # Find the maximum frequency
    max_freq = max(char_count.values())

    # Filter characters that appear more than once
    repeated_chars = [char for char, freq in char_count.items() if freq == max_freq]

    # Return a dictionary mapping each repeated character to its count
    return dict(repeated_chars)

    # Test cases to verify the correctness of the function
    assert histogram('a b c') == {'a': 1, 'b': 1, 'c': 1}
    assert histogram('a b b a') == {'a': 2, 'b': 2}
    assert histogram('a b c a b') == {'
