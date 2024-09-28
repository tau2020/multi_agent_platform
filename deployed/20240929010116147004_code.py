Here's the `calculate_factorial` function in Python, complete with documentation and input validation:

```python
def calculate_factorial(n):
    """
    Calculate the factorial of a given non-negative integer n.

    Parameters:
    n (int): A non-negative integer whose factorial is to be calculated.

    Returns:
    int: The factorial of 'n'.

    Raises:
    ValueError: If 'n' is not an integer or if it is a negative integer.

    Examples:
    >>> calculate_factorial(5)
    120

    >>> calculate_factorial(0)
    1

    >>> calculate_factorial(-1)
    Traceback (most recent call last):
    ...
    ValueError: Factorial is not defined for negative integers.
    """
    # Validate that n is an integer
    if not isinstance(n, int):
        raise ValueError("Input must be an integer.")

    # Validate that n is not negative
    if n < 0:
        raise ValueError("Factorial is not defined for negative integers.")

    # Base case: the factorial of 0 is 1
    if n == 0:
        return 1

    # Calculate the factorial iteratively
    factorial = 1
    for i in range(1, n + 1):
        factorial *= i

    return factorial

# Example usage:
# print(calculate_factorial(5))  # Should return 120
# print(calculate_factorial(0))  # Should return 1
# print(calculate_factorial(-1)) # Should raise ValueError
```

This function iteratively calculates the factorial of a non-negative integer and includes checks to ensure that the input is both an integer and non-negative. An exception is raised if either of these conditions is not met. The function can be tested by uncommenting the example usage at the bottom of the script.