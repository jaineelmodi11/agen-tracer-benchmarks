

def count_distinct_characters(string: str) -> int:
    """ Given a string, find out how many distinct characters (regardless of case) does it consist of
    >>> count_distinct_characters('xyzXYZ')
    3
    >>> count_distinct_characters('Jerry')
    4
    """
    To solve this problem, we need to iterate through each character in the string and check if it is unique. We can achieve this by converting the string into a set, which automatically removes duplicates. Here's the corrected and complete code:

    ```python
