import time
import sys
import psutil

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

def fibonacci_dp_timeout(n, timeout=10):
    start_time = time.time()
    result = fibonacci_dp(n)
    end_time = time.time()
    if end_time - start_time > timeout:
        print(f"Timeout exceeded: {end_time - start_time:.2f} seconds")
        sys.exit(1)
    return result

def fibonacci_dp_monitor(n, monitor=True):
    if monitor:
        print(f"Monitoring system resources...")
        start_time = time.time()
        result = fibonacci_dp(n)
        end_time = time.time()
        print(f"Function completed in {end_time - start_time:.2f} seconds")
        print(f"System resources:")
        print(f"  CPU usage: {psutil.cpu_percent()}%")
        print(f"  Memory usage: {psutil.virtual_memory().percent}%")
    else:
        result = fibonacci_dp(n)
    return result

def main():
    n_naive = 30
    n_dynamic = 300000  #Larger number to see the difference
    timeout = 10
    monitor = True

    start_time = time.time()
    fib_naive = fibonacci_naive(n_naive)
    end_time = time.time()
    print("Naive solution:\n")
    print(f"Function completed in {end_time - start_time:.2f} seconds for n = {n_naive}")
    print(f"Fibonacci number: {fib_naive}")

    print("\nDynamic solution:\n")

    fibonacci_dp_timeout(n_dynamic, timeout)
    result = fibonacci_dp_monitor(n_dynamic, monitor)
    if len(str(result)) < 20:
        print(f"Fibonacci number: {result}")
    else:
        print(f"Fibonacci number for sequence length {n_dynamic} has more than 20 digits, skipping printing...")

if __name__ == "__main__":
    main()