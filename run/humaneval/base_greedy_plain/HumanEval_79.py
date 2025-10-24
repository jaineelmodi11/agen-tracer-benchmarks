
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
    binary = ''
    while decimal > 0:
        remainder = decimal % 2
        binary = str(remainder) + binary
        decimal = decimal // 2
    return binary + 'db' + binary

    # Test cases
    print(decimal_to_binary(15))  # Expected output: "db1111db"
    print(decimal_to_binary(32))  # Expected output: "db100000db"
    print(decimal_to_binary(0))   # Expected output: "db0db"
    print(decimal_to_binary(1))   # Expected output: "db1db"
    print(decimal_to_binary(255)) # Expected output: "db11111111db"
