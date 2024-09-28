Here is the Python function `calculate_factorial` that you requested:

```python
def calculate_factorial(n):
    """
    Calculate the factorial of a non-negative integer n.
    
    The factorial of n, denoted as n!, is the product of all positive integers from 1 to n inclusive.
    
    Parameters:
    n (int): A non-negative integer whose factorial is to be calculated.
    
    Returns:
    int: The factorial of the given integer n.
    
    Raises:
    ValueError: If the input n is not a non-negative integer.
    
    Examples:
    >>> calculate_factorial(5)
    120
    
    >>> calculate_factorial(0)
    1
    
    >>> calculate_factorial(-1)
    ValueError: Input must be a non-negative integer.
    """
    
    # Validate that the input is a non-negative integer
    if not isinstance(n, int) or n < 0:
        raise ValueError("Input must be a non-negative integer.")
    
    # Calculate the factorial using an iterative approach
    factorial = 1
    for i in range(1, n + 1):
        factorial *= i
        
    return factorial

# Example usage:
# print(calculate_factorial(5)) # This would output 120
```

This function checks if the input `n` is a non-negative integer and calculates the factorial in an iterative manner. The iterative approach is typically efficient for handling large values, but depending on the specific use case and environment, other methods such as using memoization or built-in math libraries could also be considered for optimization.