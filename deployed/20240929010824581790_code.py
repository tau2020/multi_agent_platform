Here's a Python function that calculates the factorial of a non-negative integer using an iterative approach to avoid stack overflow issues associated with recursion for large values of `n`. The function includes detailed comments to explain its workings, and I've also provided a set of test cases to validate its correctness.

```python
def factorial(n):
    """Calculate the factorial of a non-negative integer n."""
    if n < 0:
        raise ValueError("Input must be a non-negative integer.")
    
    # Start with the base case for factorial
    result = 1
    
    # Iteratively calculate the factorial
    for i in range(2, n + 1):
        result *= i
    
    return result

# Test cases to validate the correctness of the implementation
def test_factorial():
    # Edge case
    assert factorial(0) == 1, "Test Case 1 Failed"
    assert factorial(1) == 1, "Test Case 2 Failed"
    
    # Regular cases
    assert factorial(2) == 2, "Test Case 3 Failed"
    assert factorial(3) == 6, "Test Case 4 Failed"
    assert factorial(4) == 24, "Test Case 5 Failed"
    assert factorial(5) == 120, "Test Case 6 Failed"
    
    # Larger cases
    assert factorial(10) == 3628800, "Test Case 7 Failed"
    assert factorial(20) == 2432902008176640000, "Test Case 8 Failed"

    # Very large case (to test performance)
    assert factorial(100) == 933262154439441526816992388562667004907159682643816214685929638952175999932299156089414639761565182862536979208272237582511852109168640000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000