Here's a Python function that satisfies your requirements:

```python
def calculate_factorial(n):
    """
    Calculate the factorial of a non-negative integer n.

    Parameters:
    n (int): A non-negative integer for which the factorial is to be computed.

    Returns:
    int: The factorial of the number n.

    Raises:
    ValueError: If n is negative or not an integer.
    """

    # Input validation
    if not isinstance(n, int) or n < 0:
        raise ValueError("Input must be a non-negative integer.")

    # Recursive implementation
    def factorial_recursive(k):
        # Base case: factorial of 0 is 1
        if k == 0:
            return 1
        # Recursive case
        else:
            return k * factorial_recursive(k - 1)

    return factorial_recursive(n)

# Test cases
try:
    print(calculate_factorial(5))  # Should print 120
    print(calculate_factorial(0))  # Should print 1
    print(calculate_factorial(1))  # Should print 1
    print(calculate_factorial(10)) # Should print 3628800
    # Uncomment the next line to test input validation
    # print(calculate_factorial(-1)) # Should raise ValueError
    # Uncomment the next line to test input validation
    # print(calculate_factorial(3.5)) # Should raise ValueError
except ValueError as e:
    print(e)

# Optional optimization for large n
import sys
sys.setrecursionlimit(3000) # Increase the recursion limit to allow larger values of n
```

This code provides a recursive implementation of the factorial function with input validation and a docstring explaining its usage. The test cases at the end verify that the function behaves as expected for a range of inputs, including edge cases. If you need to calculate factorials for very large values of `n`, you may need to switch to an iterative approach or use an optimized library such as `math.factorial`, which uses an efficient algorithm for large numbers and is less likely to hit recursion limits or performance bottlenecks.