Here's a Python function that calculates the factorial of a non-negative integer as per your specifications. The implementation uses an iterative approach to ensure efficiency and avoid issues with recursion depth for larger values of \( n \).

```python
def factorial(n: int) -> int:
    if n < 0:
        raise ValueError("Input must be a non-negative integer.")
    if n == 0 or n == 1:
        return 1
    
    result = 1
    for i in range(2, n + 1):
        result *= i
        
    return result

# Test cases to validate the correctness of the function
def test_factorial():
    assert factorial(0) == 1, "Test case 0 failed"
    assert factorial(1) == 1, "Test case 1 failed"
    assert factorial(2) == 2, "Test case 2 failed"
    assert factorial(3) == 6, "Test case 3 failed"
    assert factorial(4) == 24, "Test case 4 failed"
    assert factorial(5) == 120, "Test case 5 failed"
    assert factorial(6) == 720, "Test case 6 failed"
    assert factorial(10) == 3628800, "Test case 10 failed"
    assert factorial(20) == 2432902008176640000, "Test case 20 failed"
    
    print("All test cases passed!")

# Running the test cases
test_factorial()
```

### Explanation:
1. **Function Definition**:
   - The function `factorial` takes a single integer parameter `n`.
   - It checks if `n` is negative and raises a `ValueError` if so.
   - For `n = 0` or `n = 1`, it returns `1`, as defined.
   - For other values, it initializes a `result` variable to `1` and iteratively multiplies it by each integer from `2` to `n`.

2. **Test Cases**:
   - The `test_factorial` function contains a series of assert statements to verify the function's correctness across a variety of test cases, including edge cases like `0!` and `1!`, as well as the maximum case `20!`.
   - If all assertions pass, it prints a success message.

### Performance:
The function efficiently computes the factorial