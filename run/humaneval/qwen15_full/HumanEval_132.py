
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
    balance = 0
    nested = False

    for char in string:
    if char == '[':
        balance += 1
        if balance > 1:
            nested = True
    elif char == ']':
        balance -= 1
        if balance < 0:
            return False

    return nested and balance == 0
