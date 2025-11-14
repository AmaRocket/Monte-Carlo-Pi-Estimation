#!/usr/bin/env python3
"""
Monte Carlo Pi Estimation - MVP Version
Estimates Pi by randomly sampling points in a unit square
"""

import random
import time
import argparse


def estimate_pi(num_samples):
    """
    Estimate Pi using Monte Carlo method.

    Args:
        num_samples: Number of random points to generate

    Returns:
        Estimated value of Pi
    """
    inside_circle = 0

    for _ in range(num_samples):
        # Generate random point in unit square [0,1] x [0,1]
        x = random.random()
        y = random.random()

        # Check if point is inside unit circle
        if x * x + y * y <= 1.0:
            inside_circle += 1

    # Pi estimation: (points inside circle / total points) * 4
    pi_estimate = 4.0 * inside_circle / num_samples
    return pi_estimate, inside_circle


def main():
    parser = argparse.ArgumentParser(description='Monte Carlo Pi Estimation')
    parser.add_argument('-n', '--samples', type=int, default=1_000_000,
                        help='Number of samples (default: 1,000,000)')
    args = parser.parse_args()

    print("=" * 60)
    print("Monte Carlo Pi Estimation - MVP Version")
    print("=" * 60)
    print(f"Number of samples: {args.samples:,}")
    print()

    # Run estimation
    start_time = time.time()
    pi_estimate, inside = estimate_pi(args.samples)
    elapsed_time = time.time() - start_time

    # Calculate error
    import math
    error = abs(pi_estimate - math.pi)
    error_percent = (error / math.pi) * 100

    # Display results
    print("Results:")
    print(f"  Points inside circle: {inside:,}")
    print(f"  Points outside circle: {args.samples - inside:,}")
    print(f"  Estimated Pi: {pi_estimate:.10f}")
    print(f"  Actual Pi:    {math.pi:.10f}")
    print(f"  Error:        {error:.10f} ({error_percent:.4f}%)")
    print(f"  Time elapsed: {elapsed_time:.3f} seconds")
    print(f"  Samples/sec:  {args.samples / elapsed_time:,.0f}")
    print("=" * 60)


if __name__ == "__main__":
    main()