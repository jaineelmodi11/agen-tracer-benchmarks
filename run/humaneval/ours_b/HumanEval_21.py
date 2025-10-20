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

    # Create a new list with the same length as the original, but all values set to 0
    result = [0] * len(numbers)

    # Apply the transformation by subtracting the minimum value from each element and dividing by the difference between the maximum and minimum values
    for i in range(len(result)):
        result[i] = (numbers[i] - min_val) / (max_val - min_val)

    return result
