= Results and Discussion
== As $N$ Increases

#figure(
	image("../graph/jpg/comparison_all_gather.jpg"),
	caption: "Gather Merge",
)<fig-all-gather>

@fig-all-gather shows the running times of the variations of the *gather* merge
method. Based on the graph, the sequential sorting method is more performant
than spawning threads to sort it concurrently.

#figure(
	image("../graph/jpg/comparison_all_hierarchical.jpg"),
	caption: "Hierarchical Merge"
)<fig-all-hierarchical>

@fig-all-hierarchical, on the other hand, shows a different shape for the
threaded sorting with 4 threads. Threaded sorting, at smaller $N$ proves
ineffective, the overhead of spawning and distributing the arrays to threads is
expensive. Still, the sequential sorting method performs better even in this
merging method.

One thing the shapes of the two figures above fail to show is the difference of
the magnitude of these merging methods. It is properly illustrated in
@fig-all-parallel.

#figure(
	image("../graph/jpg/comparison_all_parallel.jpg"),
	caption: "Gather vs Hierarchical"
)<fig-all-parallel>

On first look, @fig-all-parallel shows the clear winner. Averaging the sorting
methods, hierarchical merging beats gather merge by a factor almost of 3.

#figure(
	image("../graph/jpg/comparison_all.jpg"),
	caption: "All Nodes Sequential vs Parallel"
)<fig-all-sequential-parallel>

@fig-all-sequential-parallel shows how sequential merge sort compares to
parallel merge sort. This figure really demonstrates why this problem is a very
parallel problem.

The previous results are all run on 23 slots, the following figures compare
running on 23 slots and on an even 16 slots.

#figure(
	image("../graph/jpg/comparison_sequential.jpg"),
	caption: "All vs Server Nodes Sequential"
)<fig-sequential>

For starters, @fig-sequential shows the worst case in the scenario -- sequential
merge sort. The cluster performs, although not significantly, but it performs
better on 16 slots than on 23.

This pattern of the 16-slot run performing better than the 23-slot run will be
visible in the following figures.

#figure(
	image("../graph/jpg/comparison_gather.jpg"),
	caption: "All vs Server Nodes Gather Merge"
)<fig-all-server-gather>

#figure(
	image("../graph/jpg/comparison_hierarchical.jpg"),
	caption: "All vs Server Nodes Hierarchical Merge"
)<fig-all-server-hierarchical>

#figure(
	image("../graph/jpg/comparison_parallel.jpg"),
	caption: "All vs Server Nodes Parallel"
)<fig-all-server-parallel>

The figures above follow the same shape -- the server nodes running slightly better than all the nodes.

== As Slots Increase

From here on, the running times will be measured as the number of slots being utilized by MPI increases.

#figure(
	image("../graph/jpg/slots_gather_expanded.jpg"),
	caption: "Parallel Gather Merge Expanded"
)<fig-gather-exp>

@fig-gather-exp shows interesting results. All sorting combinations follow a similar shape, and it's quite difficult at first look to distinguish which is which.

#figure(
	image("../graph/jpg/slots_gather_avg.jpg"),
	caption: "Parallel Gather Merge Averaged"
)<fig-gather-avg>

In @fig-gather-avg, the threaded sorting methods have been averaged out to make the situation a bit more clear. What can be made from @fig-gather-exp and @fig-gather-avg is that at 1 slot, both perform poorly. As `slots` increase early on, they both perform extremely well in comparison to the rest of the runs. 

A sweet spot, a valley can be found at `slots=6` to `slots=7`. Beyond that point, the runtimes climb high again. At the rate it's going, by 32 slots, the cluster will be performing worse than running on 1 slot.

The intriguing shape of the graph of the runtimes of the gather merge as the slots increase can be explained by @img-running-mpi.

#figure(
	image("media/mpirun with hostfile and np flag.png"),
	caption: "Running MPI with a hostfile and the -np flag"
)<img-running-mpi>

After indicating a hostfile and activating the `-np` flag, when MPI executes the code, it first sends it to itself, and then to the first hosts indicated in the hostfile, in this case, `server01` is the first host in the hostfile. That's the fastest it is supposed to be, at minimum latency. As the task is distributed to more and more computers, the latency of multiple nodes add up to a factor of why gather merge performs poorly.

#figure(
	image("../graph/jpg/slots_hierarchical_expanded.jpg"),
	caption: "Parallel Hierarchical Merge Expanded"
)<fig-hierarchical-exp>

#figure(
	image("../graph/jpg/slots_hierarchical_avg.jpg"),
	caption: "Parallel Hierarchical Merge Averaged"
)<fig-hierarchical-avg>

The two figures above show a drastically different shape from the previous
merging method. Whereas the runtimes of gather merge increased as the number of
slots increase, the runtimes of hierarchical merge fall as the number of slots
increase, a dramatic revelation.

These graphs reveal the key differences of gather and hierarchical merge. As the number of slots increase, the number of chunks that `rank 0` needs to merge also increases, and that costs its performance. Conversely for hierarchical merging, the number of slots increasing isn't a weight that `rank 0` has to carry unlike in gather merging. Hierarchical merging mirrors the way binary search tree algorithms work, it runs in logarithmic time, specifically $O(log_2n)$.