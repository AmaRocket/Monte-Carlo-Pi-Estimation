#!/bin/bash
# Manual scaling test script
# Run this to test different process counts and collect timing data

SAMPLES=${1:-10000000}  # Default 10 million samples
OUTPUT_FILE="scaling_results.txt"

echo "======================================================================" | tee $OUTPUT_FILE
echo "Manual Scaling Test - Monte Carlo Pi" | tee -a $OUTPUT_FILE
echo "======================================================================" | tee -a $OUTPUT_FILE
echo "Samples per run: $SAMPLES" | tee -a $OUTPUT_FILE
echo "" | tee -a $OUTPUT_FILE

# Test with different process counts
for NP in 1 2 4 8; do
    echo "Testing with $NP process(es)..." | tee -a $OUTPUT_FILE

    # Run and capture output
    OUTPUT=$(mpirun -np $NP python3 monte_carlo_pi_mpi.py -n $SAMPLES 2>&1)

    # Extract the timing line
    TIME_LINE=$(echo "$OUTPUT" | grep "Total time:")

    echo "  $TIME_LINE" | tee -a $OUTPUT_FILE
    echo "" | tee -a $OUTPUT_FILE
done

echo "======================================================================" | tee -a $OUTPUT_FILE
echo "Results saved to: $OUTPUT_FILE" | tee -a $OUTPUT_FILE
echo "Now run: python3 plot_scaling_results.py" | tee -a $OUTPUT_FILE
echo "======================================================================" | tee -a $OUTPUT_FILE