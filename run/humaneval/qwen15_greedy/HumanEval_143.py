
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
    To solve this problem, we need to follow these steps:

    1. Split the input sentence into individual words.
    2. Check the length of each word to determine if it is a prime number.
    3. Collect the words that are prime numbers.
    4. Join the collected words back into a single string.

    Here's the implementation of the `words_in_sentence` function:
