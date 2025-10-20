
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
    To solve this problem, we need to iterate through each word in the sentence, check if its length is a prime number, and then add it to the result string if it meets the criteria. We'll use a helper function `is_prime` to determine if a number is prime. Here's how you can implement this:

    ```python
    import math
