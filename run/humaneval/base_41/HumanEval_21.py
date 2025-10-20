from typing import List


def rescale_to_unit(numbers: List[float]) -> List[float]:
    """ Given list of numbers (of at least two elements), apply a linear transform to that list,
    such that the smallest number will become 0 and the largest will become 1
    >>> rescale_to_unit([1.0, 2.0, 3.0, 4.0, 5.0])
    [0.0, 0.25, 0.5, 0.75, 1.0]
    """
    # Find min and max values in the list
    min_val = min(numbers)
    max_val = max(numbers)

    # Create a new list with all values between 0 and 1
    return [x / (max_val - min_val) for x in numbers]# TODO: Write your code here

    # Test cases:
    test_cases = [
    ([1.0, 2.0, 3.0, 4.0, 5.0], [0.0, 0.25, 0.5, 0.75, 1.0]),
    ([1.0, 2.0, 3.0, 4.0, 5.0, 6.0], [
