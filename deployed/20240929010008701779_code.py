Certainly! Below is a Python function called `calculate_factorial` that calculates the factorial of a non-negative integer:

```python
def calculate_factorial(n):
    """
    Calculate the factorial of a non-negative integer.
    
    The factorial of a non-negative integer n is the product of all positive integers up to n.
    For example, factorial(5) would compute 5*4*3*2*1 which is 120.
    By definition, the factorial of 0 is 1.
    
    Parameters:
    n (int): A non-negative integer whose factorial is to be computed.
    
    Returns:
    int: The factorial of the input integer n.
    
    Raises:
    ValueError: If the input n is negative or not an integer.
    """
    # Validate the input
    if not isinstance(n, int):
        raise ValueError("The input must be an integer.")
    if n < 0:
        raise ValueError("The input must be a non-negative integer.")
    
    # Calculate the factorial
    factorial = 1
    for i in range(1, n + 1):
        factorial *= i
    return factorial

# Example usage:
try:
    print(calculate_factorial(5))  # Should print 120
    print(calculate_factorial(0))  # Should print 1
    # Uncomment the following line to test with an invalid input
    # print(calculate_factorial(-1))  # Should raise a ValueError
except ValueError as e:
    print("Error:", e)
```

This function starts by validating the input to ensure it's a non-negative integer. If the input is valid, it proceeds to calculate the factorial by iterating from 1 to `n` and multiplying the numbers to get the factorial. If `n` is 0, the loop does not run and the function returns 1, which is the correct factorial for 0. If the input is invalid, the function raises a `ValueError` with an appropriate message.