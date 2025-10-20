from typing import List


def mean_absolute_deviation(numbers: List[float]) -> float:
    """ For a given list of input numbers, calculate Mean Absolute Deviation
    around the mean of this dataset.
    Mean Absolute Deviation is the average absolute difference between each
    element and a centerpoint (mean in this case):
    MAD = average | x - x_mean |
    >>> mean_absolute_deviation([1.0, 2.0, 3.0, 4.0])
    1.0
    """
    To complete the `mean_absolute_deviation` function, we need to follow these steps:

    1. Calculate the mean of the input list.
    2. Compute the absolute differences from this mean for all elements in the list.
    3. Find the maximum absolute difference.
    4. Divide the maximum absolute difference by the number of elements minus one to get the mean absolute deviation.

    Here's how you can implement this:

    ```python
    from typing import List
