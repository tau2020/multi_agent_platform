Here is a Python function that matches your description:

```python
def calculate_factorial(n: int) -> int:
    """
    Calculate the factorial of a given non-negative integer.

    The factorial of a non-negative integer n is the product of all positive
    integers from 1 to n. For example, the factorial of 5 is 5*4*3*2*1 = 120.

    Parameters:
    n (int): A non-negative integer whose factorial is to be calculated.

    Returns:
    int: The factorial of the given integer n.

    Raises:
    ValueError: If n is a negative integer.
    """
    
    # Check if n is a negative integer
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers.")
    
    # The factorial of 0 is 1
    if n == 0:
        return 1
    
    # Calculate factorial using a loop
    factorial = 1
    for i in range(1, n + 1):
        factorial *= i
    
    return factorial

# Example usage:
# print(calculate_factorial(5))  # Output: 120
# print(calculate_factorial(0))  # Output: 1
# calculate_factorial(-1)  # Raises ValueError
```

This function implements an iterative approach to calculate the factorial of a given non-negative integer `n`. If `n` is negative, it raises a `ValueError`. The use of a `for` loop ensures that the code is both readable and efficient, as it minimizes the number of multiplications needed to compute the factorial.