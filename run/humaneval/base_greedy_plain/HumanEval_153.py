
def Strongest_Extension(class_name, extensions):
    """You will be given the name of a class (a string) and a list of extensions.
    The extensions are to be used to load additional classes to the class. The
    strength of the extension is as follows: Let CAP be the number of the uppercase
    letters in the extension's name, and let SM be the number of lowercase letters 
    in the extension's name, the strength is given by the fraction CAP - SM. 
    You should find the strongest extension and return a string in this 
    format: ClassName.StrongestExtensionName.
    If there are two or more extensions with the same strength, you should
    choose the one that comes first in the list.
    For example, if you are given "Slices" as the class and a list of the
    extensions: ['SErviNGSliCes', 'Cheese', 'StuFfed'] then you should
    return 'Slices.SErviNGSliCes' since 'SErviNGSliCes' is the strongest extension 
    (its strength is -1).
    Example:
    for Strongest_Extension('my_class', ['AA', 'Be', 'CC']) == 'my_class.AA'
    """
    # Your code here
    # You can use the sorted() function to sort the extensions by strength
    # and then use the first element of the sorted list as the strongest extension
    return sorted(extensions, key=lambda x: (len(x) - sum([ord(char) - ord('a') for char in x if char.isupper()]), x))[0] + '.' + class_name

    # Test cases
    print(Strongest_Extension('my_class', ['AA', 'Be', 'CC']))
    print(Strongest_Extension('my_class', ['SErviNGSliCes', 'Cheese', 'StuFfed']))
    print(Strongest_Extension('my_class', ['Slices', 'Be', 'CC']))
    print(Strongest_Extension('my_class', ['Slices', 'Be', 'CC', 'Slices']))
    print(Strongest_Extension('my_class', ['Slices', 'Be', 'CC', 'Slices', 'Slices']))
    print(Strongest_Extension('my_class', ['Slices', 'Be', 'CC', 'Slices', 'Slices', 'Slices']))
    print(Strongest_Extension('my_class', ['Slices', 'Be', 'CC', 'Slices', 'Slices', 'Slices', 'Slices']))
    print(Strongest_Extension('my_class', ['Slices', 'Be', 'CC', 'Slices', 'Slices', 'Slices', 'Slices', 'Slices']))
    print(Strongest_Extension('my_class', ['Slices', 'Be', 'CC', 'Slices', 'Slices', 'Slices', 'Slices', 'Slices', 'Slices']))
    print(Strongest_Extension('my_class', ['Slices', 'Be', 'CC', 'Slices', 'Slices', 'Slices', 'Slices', 'Slices', 'Slices', 'Slices']))
    print(Strongest_Extension('my_class', ['Slices', 'Be', 'CC', 'Slices', 'Slices', 'Slices', 'Slices', 'Slices', 'Slices', 'Slices', 'Slices']))
    print(Strongest_Extension('my_class', ['Slices', 'Be', 'CC', 'Slices', 'Slices', 'Slices', 'Slices', 'Slices', 'Slices', 'Slices', 'Slices
