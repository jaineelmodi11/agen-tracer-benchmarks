

def count_distinct_characters(string: str) -> int:
    """ Given a string, find out how many distinct characters (regardless of case) does it consist of
    >>> count_distinct_characters('xyzXYZ')
    3
    >>> count_distinct_characters('Jerry')
    4
    """
    To solve this problem, you need to convert the string into a set of its unique characters and then return the length of that set. Here's how you can implement this:

    ```python
    from collections import Counter
