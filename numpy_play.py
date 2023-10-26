import numpy as np


def print_array_details(a):
    print(f"Dimensions: {a.ndim}, shape: {a.shape}, dtype: {a.dtype}")

a = np.array([1, 2, 3, 4, 5, 6, 7, 8])

a = a.reshape([2, 4])
