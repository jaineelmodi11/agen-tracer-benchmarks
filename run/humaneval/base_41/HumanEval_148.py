
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
    # List of all planets in our solar system
    planets = ["Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"]

    # Check if the given planet names are correct
    if planet1 not in planets or planet2 not in planets:
    return ()

    # Initialize an empty list to store planets whose orbits are between the given planet names
    orbits_between = []

    # Iterate through the list of planets
    for i in range(len(planets)):
    if planets[i] == planet1 or planets[i] == planet2:
        # Add the planet to the list if it's between the given planet names
        orbits_between.append(planets[i])

    # Return a tuple containing all planets whose orbits are between the given planet names
    return tuple(or
