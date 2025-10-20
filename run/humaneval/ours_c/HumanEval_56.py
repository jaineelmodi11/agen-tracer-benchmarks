

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
    stack = []
    for char in brackets:
        if char == '<':
            stack.append(char)
        elif char == '>':
            if not stack or stack[-1] != '<':
                return False
            stack.pop()
    return len(stack) == 0


    # Test cases to verify the correctness of the function
