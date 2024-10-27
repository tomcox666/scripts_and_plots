import bisect


def longest_increasing_subsequence(arr):
    """
    Finds the longest increasing subsequence of an array in O(n log n) time.

    Args:
        arr: The input array of integers.

    Returns:
        A list representing the longest increasing subsequence.
    """
    if not arr:
        return []

    # dp[i] represents the smallest value that can end an increasing subsequence of length i+1
    dp = []
    # prev[i] stores the index of the previous element in the subsequence ending at i
    prev = [None] * len(arr)
    # pos[i] stores the position in the subsequence where element i belongs
    pos = [0] * len(arr)

    for i, num in enumerate(arr):
        # Find the position where num should be inserted
        j = bisect.bisect_left(dp, num)

        # Set the previous element index
        if j > 0:
            prev[i] = max(
                (k for k in range(i) if pos[k] == j - 1 and arr[k] < num),
                key=lambda k: arr[k],
                default=None,
            )

        # Update position
        pos[i] = j

        # If we're adding to the end, append
        if j == len(dp):
            dp.append(num)
        # Otherwise, replace the existing value
        else:
            dp[j] = num

    # Reconstruct the sequence
    result = []
    curr_pos = len(dp) - 1
    curr_idx = max(
        (i for i in range(len(arr)) if pos[i] == curr_pos), key=lambda i: arr[i]
    )

    while curr_idx is not None:
        result.append(arr[curr_idx])
        curr_idx = prev[curr_idx]

    return result[::-1]

array = [1, 2, 3, 4, 5, 7, 9, 12, 18, 2, 1, 2, 3, 4, 5, 6, 7]
result = longest_increasing_subsequence(array)

print(result)