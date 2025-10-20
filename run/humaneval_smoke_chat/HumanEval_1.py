from typing import List


def separate_paren_groups(paren_string: str) -> List[str]:
    """ Input to this function is a string containing multiple groups of nested parentheses. Your goal is to
    separate those group into separate strings and return the list of those.
    Separate groups are balanced (each open brace is properly closed) and not nested within each other
    Ignore any spaces in the input string.
    >>> separate_paren_groups('( ) (( )) (( )( ))')
    ['()', '(())', '(()())']
    """
    if char == '(':
        stack.append(i)
    elif char == ')':
        if len(stack) > 0:
            start_index = stack.pop()
            if paren_string[start_index:i] == "()":
                result.append(paren_string[start_index:i])
            else:
                # If there's no matching opening parenthesis before the closing one, add the entire substring
                result.append(paren_string[start_index:i+1])

    return result
