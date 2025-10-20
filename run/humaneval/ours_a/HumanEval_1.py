from typing import List


def separate_paren_groups(paren_string: str) -> List[str]:
    """ Input to this function is a string containing multiple groups of nested parentheses. Your goal is to
    separate those group into separate strings and return the list of those.
    Separate groups are balanced (each open brace is properly closed) and not nested within each other
    Ignore any spaces in the input string.
    >>> separate_paren_groups('( ) (( )) (( )( ))')
    ['()', '(())', '(()())']
    """
    result = []
    stack = []

    for char in paren_string:
        if char == '(':
            stack.append(char)
        elif char == ')':
            if len(stack) > 0:
                stack.pop()
            else:
                # If there's no closing parenthesis, add an empty string
                result.append('')
        else:
            # If it's an opening parenthesis, push onto the stack
            result.append(char)

    while len(stack) > 0:
        result.append('')

    return result
