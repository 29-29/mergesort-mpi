import multiprocessing as mp
from seqMergesort_np import merge, mergesort
import numpy as np

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
