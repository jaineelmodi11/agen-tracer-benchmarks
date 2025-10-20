
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
    # Count the occurrences of each character in the test string
    char_count = {}
    for char in test:
        if char in char_count:
            char_count[char] += 1
        else:
            char_count[char] = 1

    # Find the maximum occurrence and its characters
    max_occurrence = max(char_count.values())
    result = {char: occurrence for char, occurrence in char_count.items() if occurrence == max_occurrence}

    return result

    # Check function to verify the correctness of the solution
