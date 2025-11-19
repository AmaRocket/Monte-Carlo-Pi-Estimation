#!/bin/bash
# Complete demo script - runs computation and displays results

APP_DIR="/export/infoTag2025/updated_scripts/applications/monte_carlo_pi"
SCRIPTS_DIR="${APP_DIR}"
WORK_DIR="/home/radmin/monte_carlo_demo"
RESULTS_DIR="/home/radmin/monte_carlo_demo/results"

# Number of nodes to use (default: 64)
NUM_NODES=${1:-64}
SAMPLES=${2:-50000000}

echo "======================================================================="
echo "Monte Carlo Pi - Visual Cluster Demo"
echo "======================================================================="
echo "Nodes:   $NUM_NODES"
echo "Samples: $SAMPLES"
echo ""

# Create working directory
mkdir -p ${WORK_DIR}
mkdir -p ${RESULTS_DIR}

# Clean up old results
echo "Cleaning old results..."
rm -f ${RESULTS_DIR}/node_*.png

# Create hostfile
echo "Creating MPI hostfile..."
HOSTFILE="${WORK_DIR}/hostfile"

cat > $HOSTFILE << 'HOSTEOF'
10.0.0.101 slots=4
10.0.0.102 slots=4
10.0.0.103 slots=4
10.0.0.104 slots=4
10.0.0.105 slots=4
10.0.0.106 slots=4
10.0.0.107 slots=4
10.0.0.108 slots=4
10.0.0.109 slots=4
10.0.0.110 slots=4
10.0.0.111 slots=4
10.0.0.112 slots=4
10.0.0.113 slots=4
10.0.0.114 slots=4
10.0.0.115 slots=4
10.0.0.116 slots=4
10.0.0.117 slots=4
10.0.0.118 slots=4
10.0.0.119 slots=4
10.0.0.120 slots=4
10.0.0.121 slots=4
10.0.0.122 slots=4
10.0.0.123 slots=4
10.0.0.124 slots=4
10.0.0.125 slots=4
10.0.0.126 slots=4
10.0.0.127 slots=4
10.0.0.128 slots=4
10.0.0.129 slots=4
10.0.0.130 slots=4
10.0.0.131 slots=4
10.0.0.132 slots=4
10.0.0.133 slots=4
10.0.0.134 slots=4
10.0.0.135 slots=4
10.0.0.136 slots=4
10.0.0.137 slots=4
10.0.0.138 slots=4
10.0.0.139 slots=4
10.0.0.140 slots=4
10.0.0.141 slots=4
10.0.0.142 slots=4
10.0.0.143 slots=4
10.0.0.144 slots=4
10.0.0.145 slots=4
10.0.0.146 slots=4
10.0.0.147 slots=4
10.0.0.148 slots=4
10.0.0.149 slots=4
10.0.0.150 slots=4
10.0.0.151 slots=4
10.0.0.152 slots=4
10.0.0.153 slots=4
10.0.0.154 slots=4
10.0.0.155 slots=4
10.0.0.156 slots=4
10.0.0.157 slots=4
10.0.0.158 slots=4
10.0.0.159 slots=4
10.0.0.160 slots=4
10.0.0.161 slots=4
10.0.0.162 slots=4
10.0.0.163 slots=4
10.0.0.164 slots=4
HOSTEOF

TOTAL_PROCS=$((NUM_NODES * 4))

cd $SCRIPTS_DIR

# Run the computation (without sudo - SSH is configured for radmin user)
echo "Running Monte Carlo computation on $TOTAL_PROCS processes..."
echo ""

mpirun --mca btl_tcp_if_include eth0  --hostfile $HOSTFILE \
       -np $TOTAL_PROCS \
       --map-by node \
       --bind-to core \
       -x RESULTS_DIR=${RESULTS_DIR} \
       python3 visual_monte_carlo_demo.py $SAMPLES

if [ $? -eq 0 ]; then
    echo ""
    echo "Computation complete! Displaying results..."
    echo ""

    # Copy results back to APP_DIR for display
    sudo rm -rf ${APP_DIR}/results/*
    sudo cp ${RESULTS_DIR}/*.png ${APP_DIR}/results/ 2>/dev/null || cp ${RESULTS_DIR}/*.png ${APP_DIR}/results/

    # Display results
    sleep 2
    ./display_results.sh

    echo ""
    echo "======================================================================="
    echo "Demo Complete!"
    echo "======================================================================="
    echo ""
    echo "All 64 screens should now show their individual contributions."
    echo ""
    echo "To clear displays: ./clear_displays.sh"
    echo "To run again:      ./run_demo.sh [NUM_NODES] [SAMPLES]"
    echo ""
else
    echo ""
    echo "Error running computation!"
    exit 1
fi