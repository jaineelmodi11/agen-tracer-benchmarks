
def words_in_sentence(sentence):
    """
    You are given a string representing a sentence,
    the sentence contains some words separated by a space,
    and you have to return a string that contains the words from the original sentence,
    whose lengths are prime numbers,
    the order of the words in the new string should be the same as the original one.

    Example 1:
        Input: sentence = "This is a test"
        Output: "is"

    Example 2:
        Input: sentence = "lets go for swimming"
        Output: "go for"

    Constraints:
        * 1 <= len(sentence) <= 100
        * sentence contains only letters
    """
    # Split the sentence into individual words
    words = sentence.split()

    # Filter out words with length less than or equal to 3
    filtered_words = [word for word in words if len(word) > 2]

    # Sort the filtered words alphabetically
    sorted_words = sorted(filtered_words)

    # Join the sorted words back into a single string
    result = ' '.join(sorted_words)

    return result

    # Test cases
    print(words_in_sentence("This is a test"))  # Expected output: "is"
    print(words_in_sentence("lets go for swimming"))  # Expected output: "go for"import re
