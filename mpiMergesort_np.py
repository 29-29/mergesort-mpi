from mpi4py import MPI
import numpy as np
from parMergesort_np import mergeSortParallelThreads
from seqMergesort_np import merge, mergesort
import time
import multiprocessing as mp

N = 1_000_000
n = 1
lystbck = np.random.randint(1, N, N)

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# parallel
def parallelAlgorithm(lyst, gather=False, pool=False, threads=1):
	if rank == 0:
		start = time.time()
		chunks = np.array_split(lyst.copy(), size)
	else:
		chunks = None

	local_chunk = comm.scatter(chunks, root=0)

	# parallel sort on each node (via threads)
	if pool:
		local_sorted_chunk = mergeSortParallelThreads(local_chunk, threads)
	
	# sequential sort on each node
	else:
		local_sorted_chunk = mergesort(local_chunk)

	# gather merge
	if gather:
		gathered_chunks = comm.gather(local_sorted_chunk, root=0)
		if rank == 0:
			merged = gathered_chunks[0]
			for i in range(1, size):
				merged = merge(merged, gathered_chunks[i])

	# hierarchical merge
	else:
		step = 1
		while step < size:
			if rank % (2 * step) == 0:
				partner = rank + step
				if partner < size:
					recv_chunk = comm.recv(source=partner, tag=step)
					local_sorted_chunk = merge(local_sorted_chunk, recv_chunk)
			elif rank % step == 0:
				partner = rank - step
				comm.send(local_sorted_chunk, dest=partner, tag=step)
				break
			step *= 2

	if rank == 0:
		elapsed = time.time() - start
		print('Parallel: %f sec' % elapsed)

def numpyAlgorithm(lyst):
	if rank == 0:
		start = time.time()
		np.sort(lyst.copy())
		elapsed = time.time() - start
		print('NumPy sort: %f sec' % elapsed)

if __name__ == "__main__":
	# mp.set_start_method('spawn', force=True)  # Use 'spawn' for Windows compatibility
	# sequentialAlgorithm()
	parallelAlgorithm(gather=True)
	# numpyAlgorithm()
