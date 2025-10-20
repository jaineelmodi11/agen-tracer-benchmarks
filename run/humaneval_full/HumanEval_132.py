
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
    # Helper function to check if a character is inside another
    def is_inside(char, chars):
    for c in chars:
        if char == c:
            return True
    return False

    # Stack to keep track of opening brackets
    stack = []

    # Iterate through each character in the string
    for char in string:
    # If the current character is an opening bracket, push it onto the stack
    if char == '[' or char == '(' or char == '{':
        stack.append(char)
    else:
        # If the stack is empty or the top of the stack is not
