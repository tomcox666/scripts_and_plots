def find_optimal_lamp_position(block_positions, radius):
    """
    Finds the optimal position for a lamp to cover the maximum number of blocks.

    Args:
        block_positions: A list of integers representing the positions of blocks on the number line.
        radius: The radius of the lamp's light.

    Returns:
        A tuple containing the optimal lamp position and the maximum number of blocks covered.
    """

    block_positions.sort()
    n = len(block_positions)
    max_blocks_covered = 0
    optimal_position = None

    for i in range(n):
        lamp_position = block_positions[i]
        left_bound = lamp_position - radius
        right_bound = lamp_position + radius
        blocks_covered = 0

        for j in range(n):
            if left_bound <= block_positions[j] <= right_bound:
                blocks_covered += 1

        if blocks_covered > max_blocks_covered:
            max_blocks_covered = blocks_covered
            optimal_position = lamp_position

    return optimal_position, max_blocks_covered

# Example usage:
block_positions = [1, 5, 10, 12, 13, 17, 20]
radius = 3
optimal_position, max_blocks_covered = find_optimal_lamp_position(block_positions, radius)

if optimal_position is not None:
    print(f"Optimal lamp position: {optimal_position}")
    print(f"Maximum blocks covered: {max_blocks_covered}")
else:
    print("No blocks found or radius is zero.")