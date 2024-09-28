Here is the Python function `calculate_factorial` that meets your requirements:

```python
def calculate_factorial(n):
    """
    Calculate the factorial of a non-negative integer n.

    The factorial of n is the product of all positive integers from 1 to n inclusive.
    For example, factorial of 5 (5!) is 5 * 4 * 3 * 2 * 1 = 120.
    By convention, the factorial of 0 is defined to be 1.

    Parameters:
    n (int): A non-negative integer whose factorial is to be calculated.

    Returns:
    int: The factorial of the given number n.

    Raises:
    ValueError: If n is negative, as the factorial for negative numbers is undefined.
    """

    if not isinstance(n, int):
        raise TypeError("The input must be an integer.")
    
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers.")

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
    print(f"Error: {e}")
except TypeError as e:
    print(f"Error: {e}")
```

This function checks whether the input `n` is an integer and whether it is non-negative before proceeding to calculate the factorial. If the input does not meet these criteria, it raises appropriate exceptions. The factorial is calculated using a for loop that multiplies the numbers from 1 to `n` inclusive.

The example usage at the bottom shows how to call the function and handle the potential exceptions that it might raise.