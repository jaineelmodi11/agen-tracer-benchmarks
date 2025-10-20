
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
    # Initialize a counter for nested brackets
    nested_count = 0

    # Iterate through each character in the string
    for char in string:
    if char == '[':
        nested_count += 1
    elif char == ']':
        nested_count -= 1

        # If the count goes negative, it means there's no more nesting
        if nested_count < 0:
            break

    # Check if there are any remaining nested brackets
    return nested_count == 0
