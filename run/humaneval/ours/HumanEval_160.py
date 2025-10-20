
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
    # Check if there are enough operands in the operand list
    if len(operand) < 2:
    raise ValueError("Operand list must have at least two elements.")

    # Initialize the result with the first element from the operand list
    result = operand[0]

    # Iterate over each operator in the operator list
    for op in operator:
    # Perform the operation on the current result and the next element from the operand list
    result = eval(f"{op}({result})")

    return result
