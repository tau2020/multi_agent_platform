Here's the implementation of the factorial function in Python, along with some test cases to validate its correctness:

```python
def factorial(n: int) -> int:
    # Check for the input constraints
    if n < 0 or n > 20:
        raise ValueError("Input must be a non-negative integer between 0 and 20.")

    # Base cases for factorial
    if n == 0 or n == 1:
        return 1

    # Iterative approach to calculate factorial
    result = 1
    for i in range(2, n + 1):
        result *= i
    
    return result

# Example usage:
print(factorial(5))  # Output: 120
print(factorial(0))  # Output: 1
print(factorial(1))  # Output: 1
print(factorial(4))  # Output: 24
print(factorial(10)) # Output: 3628800

# Additional test cases
assert factorial(2) == 2
assert factorial(3) == 6
assert factorial(6) == 720
assert factorial(20) == 2432902008176640000  # Maximum input case
```

### Explanation:
1. **Function Definition**: The `factorial` function accepts a single parameter `n`.
2. **Input Validation**: It checks if `n` is within the valid range (0 to 20). If not, it raises a `ValueError`.
3. **Base Cases**: If `n` is 0 or 1, the function returns 1, as defined in the factorial rules.
4. **Iterative Calculation**: For values of `n` greater than 1, it calculates the factorial using a loop that multiplies the integers from 2 to `n`.
5. **Return Value**: The result is then returned.

### Testing:
- The code includes example usages and assertions that test various values of `n` to ensure the function works correctly. You can run the assertions to validate that the function behaves as expected.