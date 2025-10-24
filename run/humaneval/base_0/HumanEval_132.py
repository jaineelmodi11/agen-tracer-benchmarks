
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
    # Check if the string is empty or contains only one '['
    if not string or string[0] == '[':
    return False

    # Initialize the depth of the current nested bracket
    depth = 0

    # Iterate through the string
    for char in string:
    if char == '[':
        depth += 1
    elif char == ']':
        depth -= 1
    if depth < 0:
        # If the depth goes below zero, there is no nested bracket
        return False

    # If the depth is zero, there is at least one nested bracket
    return depth == 0
