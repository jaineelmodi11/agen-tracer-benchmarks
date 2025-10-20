
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
    # Your code here
    if number >= need:
        return [number + remaining - need, remaining]
    else:
        return [number + remaining - need, remaining]# Write your code below this line
    # print(eat(5, 6, 10))
    # print(eat(4, 8, 9))
    # print(eat(1, 10, 10))
    # print(eat(2, 11, 5))



    # Write your code above this line
    # TODO: Uncomment these import statements at the end of your script
    import sys
    sys.path.append('..')  # Add the parent directory path to the Python path for relative imports
    from helper_functions import eat


    print(eat(5
