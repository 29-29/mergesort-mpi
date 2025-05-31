#import "@preview/codelst:2.0.2": sourcecode
= Methods

This section outlines the methods and procedures used to conduct the experiment.

== Setup

The environment is set up with 4 server computers hosting 2 virtual machines
each, all connected to the network Csc175. As can be seen in @tab-server-specs,
the server computers have 8 physical cores. The virtual machines are given 2GB
of RAM each, leaving the host with 4GB of RAM. A core is dedicated to each
virtual machine, but in fact, each virtual machine uses 2 cores, one to be used
by the VM, one to run the VM itself, leaving the host with 4 cores to run its
own programs.

#let data = csv("media/tables/server_specs.csv")

#figure(
	table(
		columns: 2,
		..csv("media/tables/server_specs.csv").flatten(),
		align: left
	),
	caption: "Server Computer Specifications"
)<tab-server-specs>

#figure(
	table(
		columns: 2,
		..csv("media/tables/vm_specs.csv").flatten(),
		align: left
	),
	caption: "Virtual Machine Specifications"
)<tab-vm-specs>

The test environment, as outlined in @tab-cluster-specs, consists of 23 CPU cores in total, despite having 8 VMs, this is because one VM ran into trouble and refused to cooperate. In the end, a maximum of 23 cores ("slots" in MPI terms) were used.

#figure(
	table(
		columns: 2,
		..csv("media/tables/cluster_specs.csv").flatten(),
		align: left
	),
	caption: "Virtual Machine Specifications"
)<tab-cluster-specs>

As illustrated in @img-setup, the server computers are connected to the network
with specific IP addresses. The virtual machines are also bridged to the network
and given their own IP addresses. With this setup, one can SSH into any of the
computers or virtual machines as long as they're within the network.

#figure(image("media/setup.jpg"),caption: "Environment Setup")<img-setup>

== Merge Sort Implementation

The sequential merge sort implementation (@lst-seq-merge) used is that in Figure
3.17 of the book, "Topics in Parallel and Distributed Computing"@parallel2015.
Numpy arrays were used instead of the primitive list data type as a baseline.

The parallel implementation in Figure 3.27 of the same book@parallel2015, was
used in this project as can be seen in @lst-par-merge. This implementation
utilizes `Pool` from the `multiprocessing` library. This implementation was only
used for sorting the chunks after being scattered throughout the nodes by MPI.

Running merge sort in MPI, the array was split at the first rank, `rank == 0`,
and scattered to the ranks. As the ranks receive their chunks, they are sorted
locally using merge sort. This is where the first variable comes in.

#figure(
	caption: "Scattering Array chunks",
	sourcecode(```py
	if rank == 0:
		start = time.time()
		chunks = np.array_split(lyst.copy(), size)
	else:
		chunks = None

	local_chunk = comm.scatter(chunks, root=0)
	```)
)

=== Local Sorting Methods

There are two ways decided to sort the chunks within the process,
*sequentially*, or with `multiprocessing`, in parallel using *threads*. The code
in @lst-seq-merge was the one used for sorting sequentially, while the code in
@lst-par-merge was used to sort the array concurrently. 1, 2, and 4 threads were
used to run the sort in parallel. The program couldn't run it with 8 threads,
because it'd be running 8 threads in each CPU core, even VCPUs. In addition,
`multiprocessing` doesn't work fairly well with MPI, it's one or the other. But
in this case, `multiprocessing` was used minimally and in a far ways from MPI's
workings.

=== Merging Methods

After sorting the local chunks, there are two ways to merge them -- *gathered*
or merged *hierarchically*.

In the *gather* merging method, the sorted chunks are simply gathered back to
`rank 0`, and merged one by one there.

#figure(
	caption: "Gather Merge method",
	sourcecode(```py
		gathered_chunks:list[Any] = comm.gather(local_sorted_chunk, root=0) or []
		if rank == 0:
			merged = gathered_chunks[0]
			for i in range(1, size):
				merged = merge(merged, gathered_chunks[i])
	```)
)<lst-gather-merge>

In the *hierarchical* merging method, each process gets a partner, and each even
process receives the sorted chunk from its corresponding odd process and merges
it. This goes on until `Process 0` receives the final chunk and merges it into
itself, as illustrated in @img-hierarchical-merge. Hierarchical merging is a
very parallel algorithm.

#figure(
	caption: "Hierarchical Merge",
	image("media/hierarchical merge.jpg")
)<img-hierarchical-merge>

#figure(
	caption: "Hierarchical Merge method",
	sourcecode(```py
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
	```)
)

== Test Cases

There are two scenarios that will be captured, (a) as $N$ -- the number of
elements in the array to be sorted -- increases, in each combination of the
sorting and merging methods. (b) As the slots -- the number of processing cores
-- increases, in each combination of the sorting and merging methods.

=== As N Increases

As $N$ increases, we run the experiment on *all* the nodes available ($23
text("slots")$), and only on the *server* nodes, which have 4 slots each, giving
us an even $16 text("slots")$. The test cases to be run are the following:

#figure(
	caption: "Test Cases as N Increases",
	sourcecode(```
	server-sequential
	server-parallel-gather-sequential
	server-parallel-gather-thread-1
	server-parallel-gather-thread-2
	server-parallel-gather-thread-4
	server-parallel-hierarchical-sequential
	server-parallel-hierarchical-thread-1
	server-parallel-hierarchical-thread-2
	server-parallel-hierarchical-thread-4

	all-sequential
	all-parallel-gather-sequential
	all-parallel-gather-thread-1
	all-parallel-gather-thread-2
	all-parallel-gather-thread-4
	all-parallel-hierarchical-sequential
	all-parallel-hierarchical-thread-1
	all-parallel-hierarchical-thread-2
	all-parallel-hierarchical-thread-4
	```)
)<lst-inc-n-cases>

In the experiment proper, the number of elements in the array ranged from 10 to
1,000,000, increasing by a factor of 10 each time. Anything beyond 1,000,000
took most of the cases more than 100 seconds, too long for the impatient author.

To be able to run the program in all or on server nodes only, hostfiles were
used to specify which machines or hosts to be used by MPI.

#figure(
	caption: "Hostfile for All Nodes",
	sourcecode(```
	server01
	abdulmanan
	bucay

	server02
	badron
	mangorangca

	server03
	rosique
	# salih

	server04
	cali
	junaid
	```)
)<lst-hostfile-all>

#figure(
	caption: "Hostfile for Server Nodes",
	sourcecode(```
	server01
	server02
	server03
	server04
	```)
)<lst-hostfile-servers>

=== As slots Increase

As for as the slots increase, instead of running the experiment on all or the
server nodes, it is run on all the nodes and passed a parameter at the execution
command `-np [slots]`. Hence, it is only tested with the sequential and parallel
variations.

#figure(
	caption: "Test Cases as Slots Increase",
	sourcecode(```
	sequential
	parallel-gather-sequential
	parallel-gather-thread-1
	parallel-gather-thread-2
	parallel-gather-thread-4
	parallel-hierarchical-sequential
	parallel-hierarchical-thread-1
	parallel-hierarchical-thread-2
	parallel-hierarchical-thread-4
	```)
)<lst-inc-slots-cases>

In the experiment proper, the number of slots ranged from 1 to 24. Running it
beyond 25 caused errors with the MPI execution even with the `--oversubscribe`
flag on. The number of elements $N$ to be sorted was 1,000,000 throughout these
cases.

== Source Code and Distribution

To run the experiment, the source code had to be distributed to every working
node. To achieve this, the source code was made a repository on the machine the
researcher was working on -- * server02* -- and cloned into the other nodes.
Every time a change is made in the source code, it is pushed wherever the change
was made, and pulled by every working node. A script was written to have every
node pull the changes using MPI.

#figure(
	caption: "Pull Script",
	sourcecode(```bash
	mpirun --mca btl_tcp_if_include br0 --wdir ~/merge/ --hostfile ./merge/hostfile_sh git fetch
	mpirun --mca btl_tcp_if_include br0 --wdir ~/merge/ --hostfile ./merge/hostfile_sh git reset --hard origin/master
	```)
)

The full source code used can be found on #link("https://github.com/29-29/mergesort-mpi")[Github].
