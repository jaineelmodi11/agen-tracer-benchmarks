
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
    # Write your code here
    if not grid or not grid[0]:
        return 0
    rows = len(grid)
    cols = len(grid[0])
    left = right = 0
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == 1:
                left = max(left, j)
                right = min(right, j)
    count = 0
    while left < right:
        mid = (left + right) // 2
        total_water = 0
        for i in range(rows):
            for j in range(cols):
                if grid[i][j] > mid:
                    total_water += grid[i][j]
        if total_water >= capacity:
            left = mid
