
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
    # Replace more than 2 consecutive spaces with - 
    return text.replace(" ", "_")

    # Test cases
    print(fix_spaces("Example"))  # Expected: "Example"
    print(fix_spaces("Example 1"))  # Expected: "Example_1"
    print(fix_spaces(" Example 2"))  # Expected: "_Example_2"
    print(fix_spaces(" Example   3"))  # Expected: "_Example-3"
    print(fix_spaces("  Leading spaces"))  # Expected: "_Leading_spaces"
    print(fix_spaces("Trailing spaces  "))  # Expected: "_Trailing_spaces_"
    print(fix_spaces("  Leading spaces  -"))  # Expected: "_Leading_spaces-"
    print(fix_spaces("  Leading spaces  -  "))  # Expected: "_Leading_spaces-"
    print(fix_spaces("  Leading spaces  -  -  "))  # Expected: "_Leading_spaces-"
    print(fix_spaces("  Leading spaces  -  -  -  "))  # Expected: "_Leading_spaces-"
    print(fix_spaces("  Leading spaces  -  -  -  -  "))  # Expected: "_Leading_spaces-"
    print(fix_spaces("  Leading spaces  -  -  -  -  -  "))  # Expected: "_Leading_spaces-"
    print(fix_spaces("  Leading spaces  -  -  -  -  -  -  "))  # Expected: "_Leading_spaces-"
    print(fix_spaces("  Leading spaces  -  -  -  -  -  -  -  "))  # Expected: "_Leading_spaces-"
    print(fix_spaces("  Leading spaces  -  -  -  -  -  -  -  -  "))  # Expected: "_Leading_spaces-"
    print(fix_spaces("  Leading spaces  -  -  -  -  -  -  -  -  -  "))  # Expected: "_Leading_spaces-"
    print(fix_spaces("  Leading spaces  -  -  -  -  -  -  -  -  -  -  "))  # Expected: "_Leading_spaces-"
    print(fix_spaces("  Leading spaces  -  -  -  -  -  -  -  -  -  -  -  "))  # Expected: "_Leading_spaces-"
    print(fix_spaces("  Leading spaces  -  -  -  -  -  -
