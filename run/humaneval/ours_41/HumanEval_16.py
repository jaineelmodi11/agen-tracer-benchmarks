

def count_distinct_characters(string: str) -> int:
    """ Given a string, find out how many distinct characters (regardless of case) does it consist of
    >>> count_distinct_characters('xyzXYZ')
    3
    >>> count_distinct_characters('Jerry')
    4
    """
    To solve this problem, you can convert the string to lowercase and then count the number of unique characters using a set. Here's how you can implement it:

    ```python
