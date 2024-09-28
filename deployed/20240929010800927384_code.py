Here is a Python function that computes the factorial of a non-negative integer using an iterative approach. The function also includes error handling for invalid inputs.

```python
def factorial(n: int) -> int:
    # Check for valid input
    if n < 0 or n > 20:
        raise ValueError("Input must be a non-negative integer less than or equal to 20.")
    
    # Handle the case for 0! explicitly
    if n == 0:
        return 1
    
    # Compute factorial iteratively
    result = 1
    for i in range(1, n + 1):
        result *= i
        
    return result

# Example test cases
assert factorial(0) == 1
assert factorial(1) == 1
assert factorial(5) == 120
assert factorial(10) == 3628800

print("All test cases passed!")
```

### Explanation:
1. **Input Validation**: The function checks if the input `n` is within the valid range (0 to 20). If not, it raises a `ValueError`.
2. **Base Case**: It explicitly handles the base case `0!`, which is defined to be `1`.
3. **Iterative Calculation**: The factorial is calculated using a loop that multiplies the numbers from `1` to `n`.
4. **Return Value**: The computed factorial is returned as an integer.

### Usage:
You can call this function with any non-negative integer up to 20, and it will compute the factorial for you. The provided assertions serve as test cases to verify that the function works correctly.