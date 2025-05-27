
from mpi4py import MPI
import numpy as np
from src.mpiMergesort_np import numpyAlgorithm, parallelAlgorithm
from src.seqMergesort_np import sequentialAlgorithm
import sys

if __name__ == "__main__":
	comm = MPI.COMM_WORLD
	rank = comm.Get_rank()

	args = sys.argv[1:]
	if len(args) < 2:
		print("Usage: python main.py <algorithm> N")
		print("Algorithm options: seq(uential), par(allel), np (numpy)")
		print("N: number of elements to sort")
		sys.exit(1)

	mode = args[0]
	match (mode):
		case 'seq':
			pass
		case 'par':
			if len(args) < 4:
				print("For parallel mode, please provide the merging method: g(ather) or h(ierarchical)")
				print("Also provide the sorting method: t(hread) or s(equential)")
				sys.exit(1)
			merge_method = args[1]
			sort_method = args[2]
			if sort_method == 't':
				thread_count = 2 if len(args) < 5 else int(args[3])

	N = int(args[-1])

	if rank == 0:
		lystbck = np.random.randint(1, N, N)
		config = (mode, locals().get('merge_method', None), locals().get('sort_method', None), locals().get('thread_count', None))

	# broadcast it to node
	lystbck = comm.bcast(lystbck if rank == 0 else None, root=0)
	config = comm.bcast(config if rank == 0 else None, root=0)


	match (mode):
		case 'seq':
			if rank == 0:
				sequentialAlgorithm(lystbck)
		case 'par':
			if 'thread_count' in locals():
				parallelAlgorithm(lystbck, gather=merge_method=='g', pool=sort_method=='t', threads=thread_count)
			else:
				parallelAlgorithm(lystbck, gather=merge_method=='g', pool=sort_method=='t')
		case 'np':
			numpyAlgorithm(lystbck)