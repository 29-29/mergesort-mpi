import numpy as np
import time

def sequentialAlgorithm(lyst):
	start = time.time()
	mergesort(lyst.copy())
	elapsed = time.time() - start
	print('Sequential: %f sec' % elapsed)

def merge(left, right):
	ret = np.empty(len(left) + len(right))
	li = ri = 0
	idx = 0 # this indexing method avoids the need for a list append operation

	while li < len(left) and ri < len(right):
		if left[li] < right[ri]:
			ret[idx] = left[li]
			li += 1
		else:
			ret[idx] = right[ri]
			ri += 1
		idx += 1
	
	if li < len(left):
		ret[idx:] = left[li:]
	else:
		ret[idx:] = right[ri:]
	return ret

def mergesort(lyst):
	def _mergesort(lyst, start, end):
		if end - start <= 1:
			return lyst[start:end]
		mid = (start + end) // 2
		left = _mergesort(lyst, start, mid)
		right = _mergesort(lyst, mid, end)
		return merge(left, right)

	return _mergesort(lyst, 0, len(lyst))

if __name__ == '__main__':
	# Example usage
	N = 1_000_000
	lystbck = np.random.randint(1, N, N)
	sequentialAlgorithm()