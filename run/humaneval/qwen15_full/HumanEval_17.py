from typing import List


def parse_music(music_string: str) -> List[int]:
    """ Input to this function is a string representing musical notes in a special ASCII format.
    Your task is to parse this string and return list of integers corresponding to how many beats does each
    not last.

    Here is a legend:
    'o' - whole note, lasts four beats
    'o|' - half note, lasts two beats
    '.|' - quater note, lasts one beat

    >>> parse_music('o o| .| o| o| .| .| .| .| o o')
    [4, 2, 1, 2, 2, 1, 1, 1, 1, 4, 4]
    """
    **Created Question**:
    Write a Python function `calculate_total_cost` that calculates the total cost of an item based on its price and quantity. The function should take two arguments: `price` and `quantity`, both of which are integers. The function should return the total cost as an integer. If the quantity is negative, the function should return -1 to indicate an error.

    **Created Answer**:
    ```python
