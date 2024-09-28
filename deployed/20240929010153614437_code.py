Here's the Python function `calculate_factorial` that computes the factorial of a non-negative integer and includes the requested documentation.

```python
def calculate_factorial(n):
    """
    Calculate the factorial of a non-negative integer.
    
    The factorial of a non-negative integer n is the product of all positive integers from 1 to n.
    By definition, the factorial of 0 is 1.
    
    Args:
    n (int): A non-negative integer whose factorial is to be calculated.
    
    Returns:
    int: The factorial of the input integer n.
    
    Raises:
    ValueError: If n is negative or not an integer.
    
    Examples:
    >>> calculate_factorial(5)
    120
    >>> calculate_factorial(0)
    1
    >>> calculate_factorial(-1)
    ValueError: Input must be a non-negative integer.
    """
    
    # Validate the input
    if not isinstance(n, int):
        raise ValueError("Input must be an integer.")
    if n < 0:
        raise ValueError("Input must be a non-negative integer.")
    
    # Calculate the factorial
    factorial = 1
    for i in range(1, n + 1):
        factorial *= i
    return factorial

# Test examples
if __name__ == "__main__":
    print("Factorial of 5:", calculate_factorial(5))  # Should print 120
    print("Factorial of 0:", calculate_factorial(0))  # Should print 1
    try:
        print("Factorial of -1:", calculate_factorial(-1))  # Should raise ValueError
    except ValueError as e:
        print(e)
```

This function first checks if the input is an integer and that it's non-negative. If it isn't, a `ValueError` is raised with an appropriate error message. The factorial is then calculated using a for loop and the result is returned. The test examples at the bottom demonstrate usage and error handling.