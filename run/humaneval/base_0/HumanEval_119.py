
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
    # Initialize a counter for the balance of parentheses
    balance = 0

    # Iterate through each character in the list
    for char in lst:
    # Increment balance if it's an opening parenthesis
    if char == '(':
        balance += 1
    # Decrement balance if it's a closing parenthesis
    elif char == ')':
        balance -= 1
    else:
        # If balance is negative, it means there's a closing parenthesis before an opening one
        if balance < 0:
            return 'No'
        # Otherwise, it means there's a missing opening parenthesis
        balance += 1

    # If balance is zero, it means all parentheses are balanced
    return 'Yes' if balance == 0 else 'No'
