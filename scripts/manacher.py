def longest_palindrome_manacher(s):
    # Preprocess the string to handle even-length palindromes
    t = '#' + '#'.join(s) + '#'
    n = len(t)
    p = [0] * n  # Array to store palindrome lengths centered at each position
    center = right = 0

    for i in range(1, n - 1):
        mirror = 2 * center - i
        if i < right:
            p[i] = min(right - i, p[mirror])

        # Expand palindrome around i
        while (i + 1 + p[i] < n and i - 1 - p[i] >= 0 and
               t[i + 1 + p[i]] == t[i - 1 - p[i]]):
            p[i] += 1

        # Update center and right boundary if needed
        if i + p[i] > right:
            center = i
            right = i + p[i]

    max_len = max(p)
    center_index = p.index(max_len)
    start = (center_index - max_len) // 2  # Adjust for preprocessing
    return s[start:start + max_len]

# Example usage
string = "bananas"
result = longest_palindrome_manacher(string)
print(f"Longest palindrome in '{string}': {result}")  # Output: anana