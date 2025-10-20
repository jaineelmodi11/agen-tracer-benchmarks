from typing import List


def below_zero(operations: List[int]) -> bool:
    """ You're given a list of deposit and withdrawal operations on a bank account that starts with
    zero balance. Your task is to detect if at any point the balance of account fallls below zero, and
    at that point function should return True. Otherwise it should return False.
    >>> below_zero([1, 2, 3])
    False
    >>> below_zero([1, 2, -4, 5])
    True
    """
    To solve this problem, we need to keep track of the balance of the bank account during each operation. If at any point the balance falls below zero, we return `True`. Here's how you can implement this:

    ```python
    from typing import List
