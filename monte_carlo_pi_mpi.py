#!/usr/bin/env python3
"""
Monte Carlo Pi Estimation - MPI Parallel Version with Visualization
Distributes computation across multiple processes/nodes
"""

from mpi4py import MPI
import random
import time
import argparse
import math
import numpy as np
import matplotlib

matplotlib.use('Agg')  # Non-interactive backend for cluster
import matplotlib.pyplot as plt


def estimate_pi_worker(num_samples, rank):
    """
    Worker function: estimates Pi using assigned samples.
    Uses rank as random seed for reproducibility.
    """
    random.seed(rank)  # Different seed per process
    inside_circle = 0

    for _ in range(num_samples):
        x = random.random()
        y = random.random()

        if x * x + y * y <= 1.0:
            inside_circle += 1

    return inside_circle


def main():
    # Initialize MPI
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    # Parse arguments (only on rank 0)
    if rank == 0:
        parser = argparse.ArgumentParser(description='Monte Carlo Pi Estimation - MPI')
        parser.add_argument('-n', '--samples', type=int, default=10_000_000,
                            help='Total number of samples (default: 10,000,000)')
        args = parser.parse_args()
        total_samples = args.samples
    else:
        total_samples = None

    # Broadcast total samples to all processes
    total_samples = comm.bcast(total_samples, root=0)

    # Divide work among processes
    samples_per_process = total_samples // size
    remainder = total_samples % size

    # Distribute remainder among first processes
    if rank < remainder:
        my_samples = samples_per_process + 1
    else:
        my_samples = samples_per_process

    # Print header (only rank 0)
    if rank == 0:
        print("=" * 70)
        print("Monte Carlo Pi Estimation - MPI Parallel Version")
        print("=" * 70)
        print(f"Total samples:        {total_samples:,}")
        print(f"Number of processes:  {size}")
        print(f"Samples per process:  ~{samples_per_process:,}")
        print()

    # Synchronize before starting
    comm.Barrier()
    start_time = time.time()

    # Each process computes its portion
    local_inside = estimate_pi_worker(my_samples, rank)

    # Gather results at root
    total_inside = comm.reduce(local_inside, op=MPI.SUM, root=0)

    # Synchronize and measure time
    comm.Barrier()
    elapsed_time = time.time() - start_time

    # Display results (only rank 0)
    if rank == 0:
        pi_estimate = 4.0 * total_inside / total_samples
        error = abs(pi_estimate - math.pi)
        error_percent = (error / math.pi) * 100

        print("Results:")
        print(f"  Points inside circle: {total_inside:,}")
        print(f"  Points outside:       {total_samples - total_inside:,}")
        print(f"  Estimated Pi:         {pi_estimate:.10f}")
        print(f"  Actual Pi:            {math.pi:.10f}")
        print(f"  Error:                {error:.10f} ({error_percent:.4f}%)")
        print()
        print("Performance:")
        print(f"  Total time:           {elapsed_time:.3f} seconds")
        print(f"  Samples/sec:          {total_samples / elapsed_time:,.0f}")
        print(f"  Samples/sec/process:  {(total_samples / elapsed_time) / size:,.0f}")
        print("=" * 70)


if __name__ == "__main__":
    main()