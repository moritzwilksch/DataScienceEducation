import numpy as np
arr = np.array(range(10,20))
print(np.where(arr % 2 == 0, arr, -1))
print(np.any(arr > 20))