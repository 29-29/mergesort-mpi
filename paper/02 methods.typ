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


