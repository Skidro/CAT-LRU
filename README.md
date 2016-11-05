# CAT-LRU
This repository contains source code, execution scripts and data collected from experiments aimed at analyzing the impact of pseudo-LRU cache replacement policy on CAT partitioning.

## Hypothesis
In the RTAS-2016 paper **vCAT: Dynamic Cache Management using CAT Virtualization**, it is conjuctured that:
> It seems reasonable at first to allow a task A to access (via cache hits) cache lines in its old partitions, which are now owned by another task B. The intuition is that, if B experiences cache misses, CAT would allocate these cache lines to B; subsequently, A would experience cache misses when it attempts to access the same cache lines, and CAT would then allocate cache lines for A in its currently assigned partitions. Unfortunately, this does not always hold: for certain cache replacement policies, such as pseudo-LRU on the Intel cache, it is possible that, if A keeps aggressively accessing its content, the content will remain in the old partitions and prevent B from gaining full control over these partitions.

If the above hypothesis is indeed true (which seems reasonable), it can be a significant source of cache performance deterioration for certain co-running workload mixes. The aim of the experiment at hand is to do the following:

- Verify if the above conjucture holds true for the Intel Haswell E5-2618L v3 Platform which has CAT and pseudo-LRU
- Identify the extent to which the performance of an application can get deteriorated because of this effect

## Experiment-1
### Setup
In order to verify the first conjucture, the following experiment is devised:

- Create two mutually exclusive cache partitions in the system via CAT
- Affine a cache aggressive thread to partition-1 and let it run for some time until it has fully filled the partition with its working set
- Migrate the cache aggressive thread to partition-2 and allow it continue its execution
- Run a new thread in partition-1 which has relatively mild cache access pattern
- Monitor the utilization of cache partition-1 by the second application and its performance
- Kill the first application
- Monitor any changes in the utilization of cache partition-1 by the second application and its performance

### Constraints
- The sizes of both cache partitions and the working-set of applications should be such that that they don't make use of the ML cache
- The working set of application-2 should be small enough to fit inside its cache partition
- Application-2 should have a less aggressive cache access pattern than application-1
- Prefetchers and other performance optimization features should be disabled in hardware

### Expected Outcome
If the conjecture is true than:
- The application-2 should not be able to utilize the partition-1 to its fullest while the first application is running and should encounter cache misses
- The applicaiton-2 should be able to completely fill the partition-1 by its working set and hence experience zero misses once the application-1 has been killed
