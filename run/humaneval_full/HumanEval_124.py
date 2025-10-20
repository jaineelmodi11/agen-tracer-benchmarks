
def valid_date(date):
    """You have to write a function which validates a given date string and
    returns True if the date is valid otherwise False.
    The date is valid if all of the following rules are satisfied:
    1. The date string is not empty.
    2. The number of days is not less than 1 or higher than 31 days for months 1,3,5,7,8,10,12. And the number of days is not less than 1 or higher than 30 days for months 4,6,9,11. And, the number of days is not less than 1 or higher than 29 for the month 2.
    3. The months should not be less than 1 or higher than 12.
    4. The date should be in the format: mm-dd-yyyy

    for example: 
    valid_date('03-11-2000') => True

    valid_date('15-01-2012') => False

    valid_date('04-0-2040') => False

    valid_date('06-04-2020') => True

    valid_date('06/04/2020') => False
    """
    try:
    # Convert the input string to a datetime object
    datetime.strptime(date, '%m-%d-%Y')
    except ValueError:
    return False

    # Check if the year is within the valid range
    if datetime.now().year < 1900 or datetime.now().year > 2021:
    return False

    # Check if the month is valid
    if datetime.now().month < 1 or datetime.now().month > 12:
    return False

    # Check if the day is valid
    if datetime.now().day < 1 or datetime.now().day > 31:
    return False

    # If all checks pass, the date
