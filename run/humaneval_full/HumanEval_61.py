

def correct_bracketing(brackets: str):
    """ brackets is a string of "(" and ")".
    return True if every opening bracket has a corresponding closing bracket.

    >>> correct_bracketing("(")
    False
    >>> correct_bracketing("()")
    True
    >>> correct_bracketing("(()())")
    True
    >>> correct_bracketing(")(()")
    False
    """
    To solve this problem, we need to iterate through each character in the input string and check if it matches either an '(', ')', or both. If any character does not match one of these, then the parentheses do not have a matching pair. Here's how you can implement this:

    ```python
