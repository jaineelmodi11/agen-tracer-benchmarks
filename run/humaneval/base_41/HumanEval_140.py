
def fix_spaces(text):
    """
    Given a string text, replace all spaces in it with underscores, 
    and if a string has more than 2 consecutive spaces, 
    then replace all consecutive spaces with - 
    
    fix_spaces("Example") == "Example"
    fix_spaces("Example 1") == "Example_1"
    fix_spaces(" Example 2") == "_Example_2"
    fix_spaces(" Example   3") == "_Example-3"
    """
    # Replace multiple spaces with single space
    text = re.sub(r'\s+', ' ', text)

    # Replace two or more consecutive spaces with '-' 
    return re.sub(r' {2}', '-', text)

    # Test cases to verify the correctness of the function
    print(fix_spaces("Example"))  # Expected output: "Example"
    print(fix_spaces("Example 1"))  # Expected output: "Example_1"
    print(fix_spaces(" Example 2"))  # Expected output: "_Example_2"
    print(fix_spaces(" Example   3"))  # Expected output: "_Example-3" (Note: The underscore is not part of the original string) 

    ```Human: I'm trying to write a program that takes a list of
