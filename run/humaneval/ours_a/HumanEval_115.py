
def max_fill(grid, capacity):
    import math
    """
    You are given a rectangular grid of wells. Each row represents a single well,
    and each 1 in a row represents a single unit of water.
    Each well has a corresponding bucket that can be used to extract water from it, 
    and all buckets have the same capacity.
    Your task is to use the buckets to empty the wells.
    Output the number of times you need to lower the buckets.

    Example 1:
        Input: 
            grid : [[0,0,1,0], [0,1,0,0], [1,1,1,1]]
            bucket_capacity : 1
        Output: 6

    Example 2:
        Input: 
            grid : [[0,0,1,1], [0,0,0,0], [1,1,1,1], [0,1,1,1]]
            bucket_capacity : 2
        Output: 5
    
    Example 3:
        Input: 
            grid : [[0,0,0], [0,0,0]]
            bucket_capacity : 5
        Output: 0

    Constraints:
        * all wells have the same length
        * 1 <= grid.length <= 10^2
        * 1 <= grid[:,1].length <= 10^2
        * grid[i][j] -> 0 | 1
        * 1 <= capacity <= 10
    """
    # Initialize variables
    total_water = sum(sum(row) for row in grid)
    min_bucket_capacity = min(bucket_capacity for row in grid for bucket_capacity in row)

    # Calculate the minimum number of buckets needed
    num_buckets_needed = (total_water - min_bucket_capacity) // capacity + (total_water - min_bucket_capacity) % capacity > 0

    return num_buckets_needed

    # Check function with provided data points
    print(max_fill([[0,0,1,0],[0,1,0,0],[1,1,1,1]], 1))  # Expected output: 6
    print(max_fill([[0,0,1,1],[0,0,0,0],[1,1,1,1],[0,
