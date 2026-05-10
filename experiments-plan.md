# Experiment Plans

We would like to run the following algorithms

1. nelson_topo_iter
2. new sequential baseline (DST)
3. par_async (1,2,4,8,16,32,64,128,196 cores)
4. We could potentially include the parents list parallel benchmark
~~4. Zak's version of par_async thats actually async (1,2,4,8,16,32,64,128,196 cores) -> we can take out~~

Question: Do we want to run anything else? par_topo_iter, Nelson-Oppen(?), original parallel project from the project report

These will all be run on an ec2/Google cloud machine (TBD).

We should do 1 warmup and 5 trials for each.

We want to run on the following benchmarks

1. Random benchmarks (small-32XL) + we should do normal + deep on both
2. Synthetic benchmarks
3. Hardware (miter benchmarks)