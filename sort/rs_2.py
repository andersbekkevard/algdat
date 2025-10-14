def lsd_radix_sort(A, n, d, k):
    """Least Significant Digit Radix Sort"""
    for i in range(0, d):
        A = counting_sort_by_digit(A, n, k, i)
    return A

def msd_radix_sort(A, n, d, k):
    """Most Significant Digit Radix Sort"""
    return msd_radix_sort_helper(A, n, d-1, k)

def msd_radix_sort_helper(A, n, digit_pos, k):
    """Helper function for MSD radix sort"""
    if digit_pos < 0 or n <= 1:
        return A
    
    # Sort by current digit position
    A = counting_sort_by_digit(A, n, k, digit_pos)
    
    # Group elements by their digit value and recursively sort each group
    groups = {}
    for num in A:
        digit = (num // (10 ** digit_pos)) % 10
        if digit not in groups:
            groups[digit] = []
        groups[digit].append(num)
    
    # Recursively sort each group by the next digit position
    result = []
    for digit in sorted(groups.keys()):
        group = groups[digit]
        if len(group) > 1:
            group = msd_radix_sort_helper(group, len(group), digit_pos - 1, k)
        result.extend(group)
    
    return result

def counting_sort_by_digit(A, n, k, d):
    """Counting sort by specific digit position"""
    B = [0] * n
    C = [0] * k
    for i in range(n):
        digit = (A[i] // (10 ** d)) % 10
        C[digit] += 1
    for i in range(1, k):
        C[i] += C[i-1]
    for i in range(n-1, -1, -1):
        digit = (A[i] // (10 ** d)) % 10
        B[C[digit]-1] = A[i]
        C[digit] -= 1
    return B



if __name__ == "__main__":
    # Test cases
    test_arrays = [
        [170, 45, 75, 90, 802, 24, 2, 66],
        [1000, 100, 10, 1],
        [999, 998, 997, 996],
        [123, 456, 789, 321, 654, 987]
    ]
    
    for i, A in enumerate(test_arrays):
        n = len(A)
        d = len(str(max(A)))  # Number of digits in largest number
        k = 10  # Base 10 for decimal numbers
        
        print(f"\nTest {i+1}:")
        print("Original array:", A)
        print("LSD Radix Sort:", lsd_radix_sort(A.copy(), n, d, k))
        print("MSD Radix Sort:", msd_radix_sort(A.copy(), n, d, k))