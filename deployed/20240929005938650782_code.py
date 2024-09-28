Below is the Python function `calculate_factorial` that meets the specified requirements:

```python
def calculate_factorial(n):
    """
    Calculate the factorial of a non-negative integer n.

    Parameters:
    n (int): A non-negative integer whose factorial is to be computed.

    Returns:
    int: The factorial of the given integer n.

    Raises:
    ValueError: If n is not a non-negative integer.

    The function uses an iterative approach to calculate the factorial, which
    is more efficient and avoids stack overflows compared to the recursive approach.
    """
    if not isinstance(n, int) or n < 0:
        raise ValueError("The input must be a non-negative integer.")

    # The factorial of 0 is defined to be 1
    if n == 0:
        return 1

    # Iteratively compute the factorial
    factorial = 1
    for i in range(1, n + 1):
        factorial *= i

    return factorial

# Example usage:
try:
    print(calculate_factorial(5))  # Should print 120
except ValueError as e:
    print(e)
```

This function first checks if the input `n` is a non-negative integer and raises a `ValueError` if it is not. It then computes the factorial using an iterative approach. This is preferred over recursion for large values of `n` to avoid stack overflow errors. The function also handles the special case where the factorial of 0 is defined to be 1.