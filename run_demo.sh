#!/bin/bash
# Run Monte Carlo Pi on entire cluster, show result across all 4 panels
# To run: /export/infoTag2025/updated_scripts/applications/monte_carlo_pi/run_cluster_demo.sh [SAMPLES]

SAMPLES=${1:-50000000}

echo "========================================="
echo "Monte Carlo Pi - Cluster Demo"
echo "========================================="
echo "Nodes: 64 | Processes: 256 | Samples: $SAMPLES"
echo

# Clear Python cache on login node
rm -rf /export/infoTag2025/updated_scripts/applications/monte_carlo_pi/__pycache__

# Clear all screens, images, and Python cache on all nodes
echo "Clearing all screens and old images..."
for NODE in {101..164}; do
    ssh radmin@10.0.0.$NODE "pkill -9 feh; rm -rf /home/radmin/*.png /home/radmin/monte_carlo_demo/*.png /tmp/*.png /export/infoTag2025/updated_scripts/applications/monte_carlo_pi/__pycache__" 2>/dev/null &
done
wait
echo "All caches cleared."
echo

# Create hostfile for all 64 nodes
HOSTFILE="/tmp/cluster_hostfile"
cat > $HOSTFILE << HOSTS
$(for i in {101..164}; do echo "10.0.0.$i slots=4"; done)
HOSTS

# Run computation
mkdir -p /home/radmin/monte_carlo_demo
cd /export/infoTag2025/updated_scripts/applications/monte_carlo_pi
mpirun --mca btl_tcp_if_include eth0 --hostfile $HOSTFILE -np 256 python3 monte_carlo_summary.py $SAMPLES

# Copy result from first node (rank 0) to login node
echo
echo "Fetching result from rank 0 node..."
scp -q radmin@10.0.0.101:/home/radmin/monte_carlo_demo/cluster_result.png /home/radmin/monte_carlo_demo/

# Display result across all 4 panels
if [ -f /home/radmin/monte_carlo_demo/cluster_result.png ]; then
    echo
    ./display_on_panels.sh /home/radmin/monte_carlo_demo/cluster_result.png

    echo
    echo "========================================="
    echo "Demo Complete! All 4 panels showing result."
    echo "========================================="
else
    echo "Error: Result image not found"
fi