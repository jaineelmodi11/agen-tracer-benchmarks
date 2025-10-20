
def file_name_check(file_name):
    """Create a function which takes a string representing a file's name, and returns
    'Yes' if the the file's name is valid, and returns 'No' otherwise.
    A file's name is considered to be valid if and only if all the following conditions 
    are met:
    - There should not be more than three digits ('0'-'9') in the file's name.
    - The file's name contains exactly one dot '.'
    - The substring before the dot should not be empty, and it starts with a letter from 
    the latin alphapet ('a'-'z' and 'A'-'Z').
    - The substring after the dot should be one of these: ['txt', 'exe', 'dll']
    Examples:
    file_name_check("example.txt") # => 'Yes'
    file_name_check("1example.dll") # => 'No' (the name should start with a latin alphapet letter)
    """
    # Your code here
    return True if len(file_name) <= 3 else False if file_name.find('.') == -1 or file_name[0] != file_name[1:] else True if file_name[:2].isalpha() and file_name[-4:] in ['txt', 'exe', 'dll'] else False

    # Test cases
    print(file_name_check("example.txt")) # => 'Yes'
    print(file_name_check("1example.dll")) # => 'No'
    print(file_name_check("example.txt.txt")) # => 'Yes'
    print(file_name_check("example.txt.exe")) # => 'No'
    print(file_name_check("example.txt.dll")) # => 'No'
    print(file_name_check("example.txt.txt.txt")) # => 'Yes'
    print(file_name
