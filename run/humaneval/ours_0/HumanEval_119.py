
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
    # Initialize a counter for unmatched parentheses
    unmatched_parentheses = 0

    # Iterate through each character in the list
    for char in lst:
    # If the character is an opening parenthesis, increment the counter
    if char == '(':
        unmatched_parentheses += 1
    # If the character is a closing parenthesis, decrement the counter
    elif char == ')':
        if unmatched_parentheses > 0:
            unmatched_parentheses -= 1
        else:
            return 'No'  # No way to form a good string

    # If the counter is zero, it means all parentheses are matched
    return 'Yes' if unmatched_parentheses == 0 else 'No'
