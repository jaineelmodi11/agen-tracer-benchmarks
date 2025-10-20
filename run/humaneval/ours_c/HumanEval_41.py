

def car_race_collision(n: int):
    """
    Imagine a road that's a perfectly straight infinitely long line.
    n cars are driving left to right;  simultaneously, a different set of n cars
    are driving right to left.   The two sets of cars start out being very far from
    each other.  All cars move in the same speed.  Two cars are said to collide
    when a car that's moving left to right hits a car that's moving right to left.
    However, the cars are infinitely sturdy and strong; as a result, they continue moving
    in their trajectory as if they did not collide.

    This function outputs the number of such collisions.
    """
    # Initialize the count of collisions
    collisions = 0

    # Iterate through all possible pairs of cars
    for i in range(n):
        for j in range(i + 1, n):
            # If the cars are on opposite sides of the road, they will collide
            if (i != j) and (abs(i - j) % 2 == 1):
                collisions += 1

    return collisions

    # Example check function to verify the correctness of the solution
