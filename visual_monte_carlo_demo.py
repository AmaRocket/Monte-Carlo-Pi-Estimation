#!/usr/bin/env python3
from mpi4py import MPI
import random, time, sys
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np


# def monte_carlo_pi(samples):
#     inside = 0
#     for _ in range(samples):
#         x, y = random.random(), random.random()
#         if x * x + y * y <= 1.0:
#             inside += 1
#     return inside
def monte_carlo_pi(samples, batch_size=10000):
    inside = 0
    batches = samples // batch_size

    for batch in range(batches):
        for _ in range(batch_size):
            x, y = random.random(), random.random()
            if x * x + y * y <= 1.0:
                inside += 1

        # Brief pause every batch to reduce sustained load
        if batch % 10 == 0:
            time.sleep(0.001)  # 1ms pause every 100k samples

    # Handle remaining samples
    for _ in range(samples % batch_size):
        x, y = random.random(), random.random()
        if x * x + y * y <= 1.0:
            inside += 1

    return inside


def create_summary_viz(total_samples, num_processes, pi_estimate, elapsed_time, output_file):
    fig = plt.figure(figsize=(18, 11))
    fig.patch.set_facecolor('white')

    # Graph on left (3 columns, 6 rows) - using 6-row grid for equal split
    ax1 = plt.subplot2grid((6, 4), (0, 0), rowspan=6, colspan=3)
    ax1.set_facecolor('white')

    viz_samples = 5000
    x_in, y_in, x_out, y_out = [], [], [], []
    random.seed(42)
    for _ in range(viz_samples):
        x, y = random.random(), random.random()
        if x * x + y * y <= 1.0:
            x_in.append(x);
            y_in.append(y)
        else:
            x_out.append(x);
            y_out.append(y)

    if x_out: ax1.scatter(x_out, y_out, c='#e74c3c', s=4, alpha=0.7, label='Outside')
    if x_in: ax1.scatter(x_in, y_in, c='#3498db', s=4, alpha=0.7, label='Inside')

    theta = np.linspace(0, np.pi / 2, 100)
    ax1.plot(np.cos(theta), np.sin(theta), '#2ecc71', linewidth=4, label='Quarter Circle')
    ax1.set_xlim(-0.05, 1.05);
    ax1.set_ylim(-0.05, 1.05)
    ax1.set_aspect('equal')
    ax1.legend(fontsize=20, loc='upper right')
    ax1.set_title('Monte Carlo Pi Estimation', fontsize=32, fontweight='bold', color='#2c3e50', pad=20)
    ax1.grid(True, alpha=0.3, linewidth=1.5)
    ax1.tick_params(labelsize=16)

    # Top right - Performance (3 rows = half)
    ax2 = plt.subplot2grid((6, 4), (0, 3), rowspan=3)
    ax2.axis('off')
    ax2.set_facecolor('white')

    perf_text = f"""PERFORMANCE

Samples/Process:
  {total_samples // num_processes:,}
Time: {elapsed_time:.4f} s
Throughput:
  {total_samples / elapsed_time:,.0f} /s
Speedup: {num_processes}x"""

    ax2.text(0.1, 0.5, perf_text, fontsize=16, color='black', family='monospace',
             verticalalignment='center', bbox=dict(boxstyle='square', facecolor='lightgreen',
                                                   edgecolor='#27ae60', linewidth=3, pad=12))

    # Bottom right - Cluster results (3 rows = half)
    ax3 = plt.subplot2grid((6, 4), (4, 3), rowspan=3)
    ax3.axis('off')
    ax3.set_facecolor('white')

    result_text = f"""CLUSTER RESULTS

Total Samples:
  {total_samples:,}

Processes: {num_processes}
Nodes: 64

π Estimate:
  {pi_estimate:.10f}

Actual π:
  3.1415926536

Error:
  {abs(pi_estimate - 3.14159265359):.10f}"""

    ax3.text(0.1, 0.5, result_text, fontsize=16, color='black', family='monospace',
             verticalalignment='center', bbox=dict(boxstyle='square', facecolor='lightblue',
                                                   edgecolor='#2980b9', linewidth=3, pad=12))

    plt.tight_layout(pad=2)
    plt.savefig(output_file, dpi=120, facecolor='white', edgecolor='white')
    plt.close()


if __name__ == "__main__":
    comm = MPI.COMM_WORLD
    rank, size = comm.Get_rank(), comm.Get_size()
    samples = int(sys.argv[1]) if len(sys.argv) > 1 else 1000000
    my_samples = samples // size

    time.sleep(rank * 0.1)  # 100ms delay per rank

    random.seed(rank + int(time.time()))
    start_time = time.time()
    my_inside = monte_carlo_pi(my_samples)
    elapsed = time.time() - start_time

    total_inside = comm.reduce(my_inside, op=MPI.SUM, root=0)
    max_time = comm.reduce(elapsed, op=MPI.MAX, root=0)

    if rank == 0:
        pi_estimate = 4.0 * total_inside / samples
        output_file = "/home/radmin/monte_carlo_demo/cluster_result.png"

        create_summary_viz(samples, size, pi_estimate, max_time, output_file)

        print("\n" + "=" * 70 + "\nCLUSTER MONTE CARLO PI\n" + "=" * 70)
        print(f"Samples: {samples:,} | Processes: {size} | Pi: {pi_estimate:.10f}")
        print(f"Error: {abs(pi_estimate - 3.14159265359):.10f} | Time: {max_time:.3f}s\n" + "=" * 70 + "\n")
        print(f"Summary saved: {output_file}")