
def bf(planet1, planet2):
    '''
    There are eight planets in our solar system: the closerst to the Sun 
    is Mercury, the next one is Venus, then Earth, Mars, Jupiter, Saturn, 
    Uranus, Neptune.
    Write a function that takes two planet names as strings planet1 and planet2. 
    The function should return a tuple containing all planets whose orbits are 
    located between the orbit of planet1 and the orbit of planet2, sorted by 
    the proximity to the sun. 
    The function should return an empty tuple if planet1 or planet2
    are not correct planet names. 
    Examples
    bf("Jupiter", "Neptune") ==> ("Saturn", "Uranus")
    bf("Earth", "Mercury") ==> ("Venus")
    bf("Mercury", "Uranus") ==> ("Venus", "Earth", "Mars", "Jupiter", "Saturn")
    '''
    # Check if both planet names are valid
    if planet1.lower() != 'jupiter' and planet2.lower() != 'neptune':
        return []

    # Convert planet names to lowercase for case-insensitive comparison
    planet1 = planet1.lower()
    planet2 = planet2.lower()

    # Find the closest planet to each other
    closest_planet1 = find_closest_to(planet1)
    closest_planet2 = find_closest_to(planet2)

    # Return the tuples of planets within the given range
    return (closest_planet1 + closest_planet2) if closest_planet1 and closest_planet2 else ()

    # Test cases
    print(bf("Jupiter", "Neptune"))  # Expected output:
