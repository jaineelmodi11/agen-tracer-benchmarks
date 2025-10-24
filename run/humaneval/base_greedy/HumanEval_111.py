
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
    # Use Counter to count the occurrences of each letter
    letter_counts = Counter(test)

    # Find the letter with the highest count
    most_common_letter = letter_counts.most_common(1)[0][0]

    # Return the letter and its count
    return {most_common_letter: letter_counts[most_common_letter]}
