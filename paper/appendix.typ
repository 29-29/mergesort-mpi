#import "@preview/codelst:2.0.2": sourcecode
= Appendix
#figure(
	sourcecode(```py
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
	```),
	caption: "Sequential Merge Sort Implementation"
)<lst-seq-merge>

#figure(
	caption: "Parallel Merge Sort Implementation",
	sourcecode(```py
def mergeWrap(AandB):
	a, b = AandB
	return merge(a,b)

def mergeSortParallelThreads(lyst, n=1):
	numproc = 2**n
	endpoints = [int(x) for x in np.linspace(0, len(lyst), numproc+1, endpoint=True)]
	args = [lyst[endpoints[i]:endpoints[i+1]] for i in range(numproc)]

	with mp.Pool(processes=numproc) as pool:
		sortedsublists = pool.map(mergesort, args)

	while len(sortedsublists) > 1:
		args = [(sortedsublists[i], sortedsublists[i+1]) for i in range(0, len(sortedsublists), 2)]
		with mp.Pool(processes=numproc) as pool:
			sortedsublists = pool.map(mergeWrap, args)

	return sortedsublists[0]
	```)
)<lst-par-merge>