#!/usr/bin/env python3
"""
Scaling Test Script
Runs Monte Carlo Pi with different process counts and visualizes speedup
"""

import subprocess
import re
import matplotlib.pyplot as plt
import numpy as np
import sys


def run_mpi_test(num_processes, num_samples):
    """
    Run MPI test with specified number of processes.
    Returns execution time.
    """
    import tempfile
    import os

    # Create temporary file for visualization output
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
        tmp_file = tmp.name

    cmd = [
        'mpirun', '-np', str(num_processes),
        'python3', 'monte_carlo_pi_mpi.py',
        '-n', str(num_samples),
        '-o', tmp_file
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)

        # Clean up temp file
        try:
            os.unlink(tmp_file)
        except:
            pass

        # Extract time from output - try multiple patterns
        time_match = re.search(r'Total time:\s+([\d.]+)\s+seconds', result.stdout)
        if not time_match:
            # Try alternative pattern without extra spaces
            time_match = re.search(r'Total time:\s+([\d.]+)', result.stdout)

        if time_match:
            return float(time_match.group(1))
        else:
            print(f"\nDebug output:\n{result.stdout}")
            print(f"Warning: Could not parse time for {num_processes} processes")
            return None
    except subprocess.TimeoutExpired:
        print(f"Timeout for {num_processes} processes")
        try:
            os.unlink(tmp_file)
        except:
            pass
        return None
    except Exception as e:
        print(f"Error running test with {num_processes} processes: {e}")
        try:
            os.unlink(tmp_file)
        except:
            pass
        return None


def create_scaling_plot(process_counts, times, num_samples):
    """
    Create comprehensive scaling analysis plots.
    """
    # Calculate metrics
    speedups = [times[0] / t if t else 0 for t in times]
    efficiencies = [s / p * 100 if s else 0 for s, p in zip(speedups, process_counts)]

    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))

    # Plot 1: Execution Time
    ax1.plot(process_counts, times, 'bo-', linewidth=2, markersize=8)
    ax1.set_xlabel('Number of Processes', fontsize=11)
    ax1.set_ylabel('Execution Time (seconds)', fontsize=11)
    ax1.set_title('Execution Time vs. Number of Processes', fontsize=12, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.set_xscale('log', base=2)

    # Add value labels
    for i, (p, t) in enumerate(zip(process_counts, times)):
        ax1.annotate(f'{t:.2f}s', xy=(p, t), xytext=(5, 5),
                     textcoords='offset points', fontsize=9)

    # Plot 2: Speedup
    ax2.plot(process_counts, speedups, 'go-', linewidth=2, markersize=8, label='Actual Speedup')
    ax2.plot(process_counts, process_counts, 'r--', linewidth=2, alpha=0.7, label='Ideal Linear Speedup')
    ax2.set_xlabel('Number of Processes', fontsize=11)
    ax2.set_ylabel('Speedup Factor', fontsize=11)
    ax2.set_title('Speedup vs. Number of Processes', fontsize=12, fontweight='bold')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.set_xscale('log', base=2)
    ax2.set_yscale('log', base=2)

    # Plot 3: Parallel Efficiency
    ax3.plot(process_counts, efficiencies, 'mo-', linewidth=2, markersize=8)
    ax3.axhline(y=100, color='r', linestyle='--', linewidth=2, alpha=0.7, label='100% Efficiency')
    ax3.set_xlabel('Number of Processes', fontsize=11)
    ax3.set_ylabel('Parallel Efficiency (%)', fontsize=11)
    ax3.set_title('Parallel Efficiency vs. Number of Processes', fontsize=12, fontweight='bold')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    ax3.set_xscale('log', base=2)
    ax3.set_ylim(0, 110)

    # Plot 4: Summary Table
    ax4.axis('off')

    # Create table data
    table_data = []
    table_data.append(['Processes', 'Time (s)', 'Speedup', 'Efficiency (%)'])
    for p, t, s, e in zip(process_counts, times, speedups, efficiencies):
        table_data.append([
            str(p),
            f'{t:.3f}',
            f'{s:.2f}x',
            f'{e:.1f}%'
        ])

    table = ax4.table(cellText=table_data, cellLoc='center', loc='center',
                      colWidths=[0.2, 0.25, 0.25, 0.3])
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 2)

    # Style header row
    for i in range(4):
        table[(0, i)].set_facecolor('#3498db')
        table[(0, i)].set_text_props(weight='bold', color='white')

    # Alternate row colors
    for i in range(1, len(table_data)):
        color = '#ecf0f1' if i % 2 == 0 else 'white'
        for j in range(4):
            table[(i, j)].set_facecolor(color)

    ax4.set_title('Scaling Summary', fontsize=12, fontweight='bold', pad=20)

    # Add overall summary text
    avg_efficiency = np.mean(efficiencies)
    summary_text = f"\nTotal Samples: {num_samples:,}\nAverage Efficiency: {avg_efficiency:.1f}%"
    ax4.text(0.5, 0.05, summary_text, ha='center', fontsize=10,
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    plt.tight_layout()
    plt.savefig('scaling_analysis.png', dpi=150, bbox_inches='tight')
    print("\nScaling analysis saved to: scaling_analysis.png")

    return fig


def main():
    if len(sys.argv) > 1:
        num_samples = int(sys.argv[1])
    else:
        num_samples = 10_000_000  # Default: 10 million

    print("=" * 70)
    print("MPI Scaling Test - Monte Carlo Pi Estimation")
    print("=" * 70)
    print(f"Samples per run: {num_samples:,}")
    print()

    # Test with different process counts (adjust based on your system)
    process_counts = [1, 2, 4, 8]
    times = []

    for num_procs in process_counts:
        print(f"Running with {num_procs} process(es)... ", end='', flush=True)
        elapsed = run_mpi_test(num_procs, num_samples)

        if elapsed:
            times.append(elapsed)
            speedup = times[0] / elapsed if times else 1.0
            efficiency = (speedup / num_procs) * 100
            print(f"✓ {elapsed:.3f}s (speedup: {speedup:.2f}x, efficiency: {efficiency:.1f}%)")
        else:
            times.append(None)
            print("✗ Failed")

    # Filter out failed tests
    valid_data = [(p, t) for p, t in zip(process_counts, times) if t is not None]
    if not valid_data:
        print("\nError: No successful tests to plot")
        return

    process_counts, times = zip(*valid_data)
    process_counts = list(process_counts)
    times = list(times)

    print("\n" + "=" * 70)
    print("Generating scaling analysis visualization...")
    create_scaling_plot(process_counts, times, num_samples)
    print("=" * 70)


if __name__ == "__main__":
    main()