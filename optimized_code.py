import numpy as np

def matmul_numpy(a, b):
    a_np = np.array(a)
    b_np = np.array(b)
    return np.matmul(a_np, b_np).tolist()

def test_matmul():
    a = [[1, 1], [1, 1]]
    b = [[1, 1], [1, 1]]
    expected = [[2, 2], [2, 2]]
    result = matmul_numpy(a, b)
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
    result = matmul_numpy(a, b)
    print("Matrix multiplication complete. Time taken:", round(time.time() - start, 2), "seconds")
