
def is_bored(S):
    """
    You'll be given a string of words, and your task is to count the number
    of boredoms. A boredom is a sentence that starts with the word "I".
    Sentences are delimited by '.', '?' or '!'.
   
    For example:
    >>> is_bored("Hello world")
    0
    >>> is_bored("The sky is blue. The sun is shining. I love this weather")
    1
    """
    # Your code here

    return len([i for i in S.split('.') if 'I' in i]) 

    # Test cases
    print(is_bored("Hello world"))  # Expected output: 0
    print(is_bored("The sky is blue. The sun is shining. I love this weather"))  # Expected output: 1

    ```


    Assistant: 
    ```python3
    from typing import List
