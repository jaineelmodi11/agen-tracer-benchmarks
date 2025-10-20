from typing import List


def filter_by_prefix(strings: List[str], prefix: str) -> List[str]:
    """ Filter an input list of strings only for ones that start with a given prefix.
    >>> filter_by_prefix([], 'a')
    []
    >>> filter_by_prefix(['abc', 'bcd', 'cde', 'array'], 'a')
    ['abc', 'array']
    """
    raise TypeError("The 'strings' parameter must be a list.")
    if not isinstance(prefix, str):
    raise TypeError("The 'prefix' parameter must be a string.")

    # Use a generator expression to create the filtered list
    return (s for s in strings if s.startswith
