import numpy as np

def matmul(a, b):
    result = [[0 for _ in range(len(b[0]))] for _ in range(len(a))]
    for i in range(len(a)):
        for j in range(len(b[0])):
            for k in range(len(b)):
                result[i][j] += a[i][k] * b[k][j]
    return result

def test_matmul():
    a = [[1, 1], [1, 1]]
    b = [[1, 1], [1, 1]]
    expected = [[2, 2], [2, 2]]
    result = matmul(a, b)
    assert result == expected, f"Expected {expected}, got {result}"
    print("Test passed: matmul produces correct result.")

if __name__ == "__main__":
    test_matmul()
    # Larger matrices for perf measurement
    import random
    import time
    size = 100
    a = [[random.random() for _ in range(size)] for _ in range(size)]
    b = [[random.random() for _ in range(size)] for _ in range(size)]
    start = time.time()
    result = matmul(a, b)
    print("Matrix multiplication complete. Time taken:", round(time.time() - start, 2), "seconds")

