# trace

This repo contains different python implementations of cache replacement algorithms, working on a trace of strings that represents a page access order from a real system.
These scripts where used to motivate which algorithm to implement in the Neo4j Kernel.

Notably the current eviction algorithm that Neo4j uses closely resembles the algorithm of clock_4_usage.py

The scripts run the algorithms single threaded and are therefore not exactly a carbon copy of what you would implement in reality

To implement your own replacement strategy you can start by copying the trace-scan.py file, where we show how to scan the page trace into a datastructure that you can then implement your strategy on.

to run all the replacement algorithms here on the default trace you can run the run.sh script. You may need to give the script executeable permissions. 

chmod +x run.sh

The script will prompt you for what trace to run, cache size of the runs and if you want to run the "optimal" calculation according to the belady unrealizeable algorithm, which takes a while, scaling by n² with trace size (roughly)