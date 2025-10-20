
def match_parens(lst):
    '''
    You are given a list of two strings, both strings consist of open
    parentheses '(' or close parentheses ')' only.
    Your job is to check if it is possible to concatenate the two strings in
    some order, that the resulting string will be good.
    A string S is considered to be good if and only if all parentheses in S
    are balanced. For example: the string '(())()' is good, while the string
    '())' is not.
    Return 'Yes' if there's a way to make a good string, and return 'No' otherwise.

    Examples:
    match_parens(['()(', ')']) == 'Yes'
    match_parens([')', ')']) == 'No'
    '''
    # Initialize counters for opening and closing parentheses
    open_count = 0
    close_count = 0

    # Iterate through each character in the list
    for char in lst:
    if char == '(':
        open_count += 1
    elif char == ')':
        close_count += 1

    # If either count goes above 2, it means we cannot form a valid sequence
    if open_count > 2 or close_count > 2:
        return 'No'

    # If both counts are
