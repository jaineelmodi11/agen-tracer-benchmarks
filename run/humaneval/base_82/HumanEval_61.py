

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
    stack = []
    for char in brackets:
        if char == '(':
            stack.append(char)
        elif char == ')':
            if not stack or stack[-1] != '(':
                return False
            else:
                stack.pop()
    return len(stack) == 0


    # def check_brackets(brackets: str):
    #     """brackets is a string of parentheses. 
    #     returns True if the brackets are balanced, otherwise False."""
    #     balance = 0
    #     for char in brackets:
    #         if char == '(':
    #             balance += 1
    #         elif char == ')':
    #             balance -= 1
    #     return balance == 0

    # def check_brackets(brackets: str):
    #     """brackets is
