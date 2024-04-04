import time

def fibonacci_naive(n):
    if n <= 1:
        return n
    else:
        return fibonacci_naive(n-1) + fibonacci_naive(n-2)

def fibonacci_dp(n):
    table = [0, 1] + [0]*(n-1)
    for i in range(2, n+1):
        table[i] = table[i-1] + table[i-2]
    return table[n]

n_naive = 30
n_dynamic = 30000  #Larger number to see the difference

start_time = time.time()
fib_naive = fibonacci_naive(n_naive)
end_time = time.time()
print(f"Naive approach: {end_time - start_time:.2f} seconds | n = {n_naive}")

start_time = time.time()
fib_dp = fibonacci_dp(n_dynamic)
end_time = time.time()
print(f"Dynamic programming approach: {end_time - start_time:.2f} seconds | n = {n_dynamic}")

print(f"Fibonacci number: {fib_naive} (naive), {fib_dp} (dynamic programming)")