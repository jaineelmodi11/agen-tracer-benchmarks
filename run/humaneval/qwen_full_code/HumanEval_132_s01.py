
def is_nested(string):
    '''
    Create a function that takes a string as input which contains only square brackets.
    The function should return True if and only if there is a valid subsequence of brackets 
    where at least one bracket in the subsequence is nested.

    is_nested('[[]]') ➞ True
    is_nested('[]]]]]]][[[[[]') ➞ False
    is_nested('[][]') ➞ False
    is_nested('[]') ➞ False
    is_nested('[[][]]') ➞ True
    is_nested('[[]][[') ➞ True
    '''
    stack = []
    max_depth = 0
    current_depth = 0

    for char in string:
        if char == '[':
            stack.append(char)
            current_depth += 1
            max_depth = max(max_depth, current_depth)
        elif char == ']':
            if stack:
                stack.pop()
                current_depth -= 1
            else:
                # If stack is empty, it means there's an unmatched closing bracket
                return False

    # A valid sequence has at least one nested bracket
    return max_depth > 1
