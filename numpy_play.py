import numpy as np


def print_array_details(a):
    print(f"Dimensions: {a.ndim}, shape: {a.shape}, dtype: {a.dtype}")

# creates numpy arr
a = np.array([1, 2, 3, 4, 5, 6, 7, 8])

#converts to a 2d array with 2 rows, 4 columns
a = a.reshape([2, 4])

# np has a great random module too
r = np.random.random((2,3))

# previously did this by hand in QuantEcon
b = np.linspace([2,10,5])

# similar to linspace but with steps rather than interpolating
c = np.arange(2,10,2)

# misc math functions
pi = np.pi
a = np.array([pi, pi/2, pi/4, pi/6])
degs = np.degrees(a)
sin_a = np.sin(a)
rounded = np.round(sin_a, 7)
a = np.arange(8).reshape(2,4)
c_sum = np.cumsum(a, axis=1) # cum sum for each arr
c_sum_flat = np.cumsum(a) # flattens arrs by default

def moving_average(a, n=3):
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n

a = np.arange(10)
moving_average(a, 4)
