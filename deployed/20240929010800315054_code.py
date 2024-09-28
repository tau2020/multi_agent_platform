Here's a Python function that computes the factorial of a non-negative integer, adhering to the specifications you've provided:

```python
def factorial(n: int) -> int:
    # Check if n is an integer
    if not isinstance(n, int):
        raise TypeError("Input must be a non-negative integer.")
    
    # Check for valid range
    if n < 0:
        raise ValueError("Input must be a non-negative integer.")
    if n > 20:
        raise ValueError("Input exceeds the maximum allowed value of 20.")
    
    # Calculate factorial using an iterative approach
    result = 1
    for i in range(2, n + 1):
        result *= i
    
    return result

# Example usage:
print(factorial(5))  # Output: 120
print(factorial(0))  # Output: 1
print(factorial(10)) # Output: 3628800
```

### Explanation:
1. **Input Validation**: The function first checks if the input is a non-negative integer. If not, it raises appropriate exceptions (`TypeError` or `ValueError`).
2. **Factorial Calculation**: It uses an iterative approach to calculate the factorial, which is efficient for the given input range (0 to 20).
3. **Return Value**: The function returns the computed factorial as an integer.

### Error Handling:
- The function raises a `TypeError` if the input is not an integer.
- It raises a `ValueError` if the input is negative or greater than 20.

This implementation ensures that the function is robust and handles edge cases effectively.