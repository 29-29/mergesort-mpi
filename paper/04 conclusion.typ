= Conclusion

This paper set out to investigate the problem of optimizing merge sort, knowing
it requires the application of parallel computing. This experiment shows the
exponential advantage that parallel algorithms put on the table, especially with
larger arrays. This experiment revealed the nuances of different ways to do a
parallel merge sort algorithm.

The findings suggest that parallel algorithms can also be partially sequential, and going the parallel route will only garner better gains, as was observed in the gather and hierarchical merging methods. Although, not all parallel applications bring improvement to the performance of the algorithm, as we saw with the threaded sorting and sequential sorting. This goes to show that in-depth analysis of a parallel algorithm is required when looking to utilize one as some parallel methods come with their own costs and tradeoffs.

This study still acknowledges that it is limited by a couple or more factors such as the hardware available and the network configuration, among other things unknown to the author. Some points of suggestion for further research would be to implement this in a cloud environment with virtually unlimited resources to really get down dirty with the merge sort algorithm.