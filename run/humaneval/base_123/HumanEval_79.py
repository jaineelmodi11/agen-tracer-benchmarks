
def decimal_to_binary(decimal):
    """You will be given a number in decimal form and your task is to convert it to
    binary format. The function should return a string, with each character representing a binary
    number. Each character in the string will be '0' or '1'.

    There will be an extra couple of characters 'db' at the beginning and at the end of the string.
    The extra characters are there to help with the format.

    Examples:
    decimal_to_binary(15)   # returns "db1111db"
    decimal_to_binary(32)   # returns "db100000db"
    """
    if not isinstance(decimal, int):
        raise ValueError("Input must be an integer")

    binary = ""
    while decimal > 0:
        remainder = decimal % 2
        binary = str(remainder) + binary
        decimal //= 2

    return f"db{binary}db"

    # Example usage:
    print(decimal_to_binary(15))  # Output: db1111db
    print(decimal_to_binary(32))  # Output: db100000db
    ```

    This code snippet defines a function `decimal_to_binary` that takes an integer as input and returns its binary representation as a string. It handles edge cases such as non-integer inputs by raising a `ValueError`. The function uses a loop to repeatedly divide
