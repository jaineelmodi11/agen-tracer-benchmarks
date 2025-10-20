from typing import List


def has_close_elements(numbers: List[float], threshold: float) -> bool:
    """ Check if in given list of numbers, are any two numbers closer to each other than
    given threshold.
    >>> has_close_elements([1.0, 2.0, 3.0], 0.5)
    False
    >>> has_close_elements([1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.3)
    True
    """
    for j in range(i + 1, len(numbers)):
        # Calculate the absolute difference between the current pair
        diff = abs(numbers[i] - numbers[j])
        # If the difference is less than or equal to the threshold, return True
        if diff <= threshold:
            return True
    # If no such pair was found, return False
    return False
