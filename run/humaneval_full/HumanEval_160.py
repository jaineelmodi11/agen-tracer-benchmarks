
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
    # Check if the lengths of both lists match
    if len(operator) != len(operand) - 1:
    raise ValueError("The lengths of the operator and operand lists must be equal.")

    # Initialize the result with the first element from the operand list
    result = operand[0]

    # Iterate through each element in the operand list
    for i in range(len(operand)):
    # Apply the operator on the current element from the operand list
    result += operator[i] * operand[i+1]

    return result
