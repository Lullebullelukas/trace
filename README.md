# trace

This repo contains different python implementations of cache replacement algorithms, working on a trace of strings that represents a page access order from a real system.
These scripts where used to motivate which algorithm to implement in the Neo4j Kernel.

Notably the current eviction algorithm that Neo4j uses closely resembles the algorithm of clock_4_usage.py

The scripts run the algorithms single threaded and are therefore not exactly a carbon copy of what you would implement in reality
