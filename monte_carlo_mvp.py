#!/usr/bin/env python3
"""
Monte Carlo Pi Estimation with Visualization
Creates visual representation of the Monte Carlo method
"""

import random
import time
import argparse
import math
import matplotlib.pyplot as plt
import numpy as np


def estimate_pi_with_points(num_samples, visualize_samples=5000):
    """
    Estimate Pi and optionally return points for visualization.

    Args:
        num_samples: Total number of samples
        visualize_samples: Number of points to save for visualization (max)

    Returns:
        pi_estimate, inside_count, points_for_viz (x_in, y_in, x_out, y_out)
    """
    inside_circle = 0

    # Storage for visualization points
    x_inside = []
    y_inside = []
    x_outside = []
    y_outside = []

    save_points = num_samples <= visualize_samples

    for i in range(num_samples):
        x = random.random()
        y = random.random()

        if x * x + y * y <= 1.0:
            inside_circle += 1
            if save_points or len(x_inside) < visualize_samples // 2:
                x_inside.append(x)
                y_inside.append(y)
        else:
            if save_points or len(x_outside) < visualize_samples // 2:
                x_outside.append(x)
                y_outside.append(y)

    pi_estimate = 4.0 * inside_circle / num_samples

    return pi_estimate, inside_circle, (x_inside, y_inside, x_outside, y_outside)


def create_visualization(points, pi_estimate, num_samples, elapsed_time, filename='monte_carlo_pi.png'):
    """
    Create a visualization of the Monte Carlo method.
    """
    x_inside, y_inside, x_outside, y_outside = points

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Left plot: Point distribution
    ax1.scatter(x_outside, y_outside, c='red', s=1, alpha=0.5, label='Outside circle')
    ax1.scatter(x_inside, y_inside, c='blue', s=1, alpha=0.5, label='Inside circle')

    # Draw the quarter circle
    theta = np.linspace(0, np.pi / 2, 100)
    circle_x = np.cos(theta)
    circle_y = np.sin(theta)
    ax1.plot(circle_x, circle_y, 'g-', linewidth=2, label='Quarter circle')

    ax1.set_xlim(0, 1)
    ax1.set_ylim(0, 1)
    ax1.set_aspect('equal')
    ax1.set_xlabel('X', fontsize=12)
    ax1.set_ylabel('Y', fontsize=12)
    ax1.set_title('Monte Carlo Point Distribution', fontsize=14, fontweight='bold')
    ax1.legend(loc='upper right')
    ax1.grid(True, alpha=0.3)

    # Right plot: Results summary
    ax2.axis('off')

    error = abs(pi_estimate - math.pi)
    error_percent = (error / math.pi) * 100

    results_text = f"""
Monte Carlo Pi Estimation Results

Total Samples: {num_samples:,}
Points Inside Circle: {len(x_inside):,}
Points Outside Circle: {len(x_outside):,}

Estimated π: {pi_estimate:.10f}
Actual π:    {math.pi:.10f}
Error:       {error:.10f}
Error %:     {error_percent:.4f}%

Computation Time: {elapsed_time:.3f} seconds
Samples/second:   {num_samples / elapsed_time:,.0f}

Formula: π ≈ 4 × (points inside / total points)
"""

    ax2.text(0.1, 0.5, results_text, fontsize=11, family='monospace',
             verticalalignment='center', bbox=dict(boxstyle='round',
                                                   facecolor='wheat', alpha=0.5))

    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    print(f"\nVisualization saved to: {filename}")

    return fig


def main():
    parser = argparse.ArgumentParser(description='Monte Carlo Pi Estimation with Visualization')
    parser.add_argument('-n', '--samples', type=int, default=100_000,
                        help='Number of samples (default: 100,000)')
    parser.add_argument('-o', '--output', type=str, default='monte_carlo_pi.png',
                        help='Output filename for visualization (default: monte_carlo_pi.png)')
    parser.add_argument('--no-display', action='store_true',
                        help='Do not display plot window (only save to file)')
    args = parser.parse_args()

    print("=" * 70)
    print("Monte Carlo Pi Estimation with Visualization")
    print("=" * 70)
    print(f"Number of samples: {args.samples:,}")
    print("\nRunning simulation...")

    # Run estimation
    start_time = time.time()
    pi_estimate, inside, points = estimate_pi_with_points(args.samples)
    elapsed_time = time.time() - start_time

    # Display text results
    error = abs(pi_estimate - math.pi)
    error_percent = (error / math.pi) * 100

    print("\nResults:")
    print(f"  Estimated Pi: {pi_estimate:.10f}")
    print(f"  Actual Pi:    {math.pi:.10f}")
    print(f"  Error:        {error:.10f} ({error_percent:.4f}%)")
    print(f"  Time elapsed: {elapsed_time:.3f} seconds")

    # Create visualization
    print("\nGenerating visualization...")
    fig = create_visualization(points, pi_estimate, args.samples,
                               elapsed_time, args.output)

    if not args.no_display:
        plt.show()

    print("=" * 70)


if __name__ == "__main__":
    main()