

def correct_bracketing(brackets: str):
    """ brackets is a string of "<" and ">".
    return True if every opening bracket has a corresponding closing bracket.

    >>> correct_bracketing("<")
    False
    >>> correct_bracketing("<>")
    True
    >>> correct_bracketing("<<><>>")
    True
    >>> correct_bracketing("><<>")
    False
    """
    return len(brackets) % 2 == 0 and all(brackets[i] == '>' for i in range(0, len(brackets), 2)) and all(brackets[i] == '<' for i in range(1, len(brackets), 2))
