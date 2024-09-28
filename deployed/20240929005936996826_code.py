```python
def calculate_factorial(n):
    """
    Calculate the factorial of a non-negative integer n.
    
    The factorial of n (denoted as n!) is the product of all positive integers up to n.
    By definition, the factorial of 0 is 1.
    
    Parameters:
    n (int): A non-negative integer whose factorial is to be computed.
    
    Returns:
    int: The factorial of the given non-negative integer n.
    
    Raises:
    ValueError: If n is negative or not an integer.
    """
    
    # Check if n is an integer and non-negative
    if not isinstance(n, int) or n < 0:
        raise ValueError("Input must be a non-negative integer.")
    
    # Factorial of 0 is defined as 1
    if n == 0:
        return 1
    
    # Calculate factorial using a loop
    factorial = 1
    for i in range(1, n + 1):
        factorial *= i
        
    return factorial

# Example usage:
try:
    print(calculate_factorial(5))  # Should print 120
    print(calculate_factorial(0))  # Should print 1
    print(calculate_factorial(-1)) # Should raise ValueError
except ValueError as e:
    print(e)
```

This function `calculate_factorial` will correctly calculate the factorial of the input `n` if it is a non-negative integer, otherwise, it will raise a `ValueError` with a message "Input must be a non-negative integer." The example usage at the end demonstrates how to call the function and handle potential exceptions.