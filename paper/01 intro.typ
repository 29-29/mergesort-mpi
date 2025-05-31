= Introduction

The merge sort algorithm is a divide-and-conquer sorting algorithm that works by
recursively splitting the array to two halves, sorting it, and merging it back
to obtain the sorted array@geeks-merge. This article@w3-merge by W3schools better
illustrates how merge sort works

In the discussion of optimizing the merge sort algorithm, the application of
parallelism to the algorithm is inevitable. The nature of the algorithm exudes a
stench that begs to be parallelized. In Python, merge sort can be parallelized
within a computer using threads with the `multiprocessing` library. The
limitations stands that the resources that can be used by the program are those
present in the machine it's running in.

Introducing MPI, Message Passing Interface, a standard specification of
message-passing interface for parallel computation in distributed-memory
systems@nmsu_mpi. In simpler terms, MPI is a library that has functions that
allow developers to write programs for parallel systems. Ports of the library
for other languages such as in Python's `mpi4py` allows developers of various
disciplines to write parallel programs.

This paper sets out to investigate a couple of ways to sort a `numpy` array in
Python with OpenMPI and `mpi4py`, and explore locally optimal ways to sort an
array.