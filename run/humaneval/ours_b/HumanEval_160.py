
def do_algebra(operator, operand):
    """
    Given two lists operator, and operand. The first list has basic algebra operations, and 
    the second list is a list of integers. Use the two given lists to build the algebric 
    expression and return the evaluation of this expression.

    The basic algebra operations:
    Addition ( + ) 
    Subtraction ( - ) 
    Multiplication ( * ) 
    Floor division ( // ) 
    Exponentiation ( ** ) 

    Example:
    operator['+', '*', '-']
    array = [2, 3, 4, 5]
    result = 2 + 3 * 4 - 5
    => result = 9

    Note:
        The length of operator list is equal to the length of operand list minus one.
        Operand is a list of of non-negative integers.
        Operator list has at least one operator, and operand list has at least two operands.

    """
    # Initialize the result with the first element from the operand list
    result = operand[0]

    # Iterate over each element in the operator list
    for op in operator:
        if op == '+':
            result += operand[1]  # Add the next element in the operand list to the current result
        elif op == '-':
            result -= operand[1]  # Subtract the next element in the operand list from the current result
        elif op == '*':
            result *= operand[1]  # Multiply the current result by the next element in the operand list
        elif op == '//':
            result //= operand[1]  # Divide the current result by the next element in the operand list
        elif op == '**':
            result **=
