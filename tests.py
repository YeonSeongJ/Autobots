import numpy as np

nplist = np.array([1,3,4,2,3,4,5,3,2,2,5,6,8,5,4,3,3,5,5,7,4,4,3,3,6,7])
nplist = np.array([1,1,1,1,2,2,3,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4,4,4,5,5,6,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9])

unique, counts = np.unique(nplist, return_counts=True)

result = dict(zip(counts, unique))
result = result[max(result)]
print(result)