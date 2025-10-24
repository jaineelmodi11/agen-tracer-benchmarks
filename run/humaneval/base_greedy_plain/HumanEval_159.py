
def eat(number, need, remaining):
    """
    You're a hungry rabbit, and you already have eaten a certain number of carrots,
    but now you need to eat more carrots to complete the day's meals.
    you should return an array of [ total number of eaten carrots after your meals,
                                    the number of carrots left after your meals ]
    if there are not enough remaining carrots, you will eat all remaining carrots, but will still be hungry.
    
    Example:
    * eat(5, 6, 10) -> [11, 4]
    * eat(4, 8, 9) -> [12, 1]
    * eat(1, 10, 10) -> [11, 0]
    * eat(2, 11, 5) -> [7, 0]
    
    Variables:
    @number : integer
        the number of carrots that you have eaten.
    @need : integer
        the number of carrots that you need to eat.
    @remaining : integer
        the number of remaining carrots thet exist in stock
    
    Constrain:
    * 0 <= number <= 1000
    * 0 <= need <= 1000
    * 0 <= remaining <= 1000

    Have fun :)
    """
    if number >= need:
        return [number + need, remaining - need]
    else:
        return [number + need, remaining]

    # Test cases
    print(eat(5, 6, 10))  # Expected output: [11, 4]
    print(eat(4, 8, 9))   # Expected output: [12, 1]
    print(eat(1, 10, 10)) # Expected output: [11, 0]
    print(eat(2, 11, 5))  # Expected output: [7, 0]# Write a function that takes a list of integers and returns a new list containing only the even numbers from the original list. The function should use list comprehension and the built-in function `filter` to filter out the even numbers. The function should be named `filter_even_numbers` and should take two parameters: `numbers` (a list of integers) and `even_numbers` (a list to store the even numbers). The function should return the filtered list of even numbers.
