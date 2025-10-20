
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
    # Initialize an empty dictionary to store the result
    histogram_dict = {}

    # Iterate through each character in the test string
    for char in test.split():
    # If the character is already in the dictionary, increment its count
    if char in histogram_dict:
        histogram_dict[char] += 1
    else:
        # Otherwise, add the character to the dictionary with a count of 1
        histogram_dict[char] = 1

    # Return the dictionary containing the most frequent characters and their counts
    return {k
