

def how_many_times(string: str, substring: str) -> int:
    """ Find how many times a given substring can be found in the original string. Count overlaping cases.
    >>> how_many_times('', 'a')
    0
    >>> how_many_times('aaa', 'a')
    3
    >>> how_many_times('aaaa', 'aa')
    3
    """
        # If there's an overlap, increment the count
        if string[start_index:start_index + len(substring)] == substring:
            count += 1
        start_index += 1

    else:
        break

    return count
