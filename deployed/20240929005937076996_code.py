Here's a Python function named `calculate_factorial` that calculates the factorial of a given non-negative integer using an iterative approach for efficiency. The function checks for valid input and raises a `ValueError` with a descriptive message in case of invalid input.

```python
def calculate_factorial(n):
    if not isinstance(n, int) or n < 0:
        raise ValueError("Input must be a non-negative integer.")
    
    factorial = 1
    for i in range(1, n + 1):
        factorial *= i
    return factorial

# Example usage:
try:
    print(calculate_factorial(5))  # Output: 120
    print(calculate_factorial(0))  # Output: 1
    print(calculate_factorial(-1)) # This will raise an exception
except ValueError as e:
    print(e)
```

If you would prefer a recursive implementation, here is an alternative version that uses recursion:

```python
def calculate_factorial(n):
    if not isinstance(n, int) or n < 0:
        raise ValueError("Input must be a non-negative integer.")
    
    if n == 0:
        return 1
    else:
        return n * calculate_factorial(n - 1)

# Example usage:
try:
    print(calculate_factorial(5))  # Output: 120
    print(calculate_factorial(0))  # Output: 1
    print(calculate_factorial(-1)) # This will raise an exception
except ValueError as e:
    print(e)
```

Both versions will work correctly, but the iterative version is generally preferred for large values of `n` to avoid hitting Python's recursion depth limit and to be more memory-efficient.