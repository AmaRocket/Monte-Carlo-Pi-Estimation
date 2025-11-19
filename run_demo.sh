#!/bin/bash
# Run Monte Carlo Pi on entire cluster, show one result on all screens

SAMPLES=${1:-50000000}

echo "========================================="
echo "Monte Carlo Pi - Cluster Demo"
echo "========================================="
echo "Nodes: 64 | Processes: 256 | Samples: $SAMPLES"
echo

# Clear all screens and ALL png files first
echo "Clearing all screens and old images..."
for NODE in {101..164}; do
    ssh radmin@10.0.0.$NODE "pkill -9 feh; rm -f /home/radmin/*.png /home/radmin/monte_carlo_demo/*.png /home/radmin/monte_carlo_demo/results/*.png" 2>/dev/null &
done
wait
echo "Screens cleared."
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

# Copy result to all nodes
if [ -f /home/radmin/monte_carlo_demo/cluster_result.png ]; then
    echo "Distributing result to all nodes..."
    for NODE in {101..164}; do
        scp -q /home/radmin/monte_carlo_demo/cluster_result.png radmin@10.0.0.$NODE:/home/radmin/cluster_result.png &
    done
    wait

    # Small delay to ensure files are written
    sleep 1

    echo "Displaying on all 64 screens..."
    for NODE in {101..164}; do
        ssh radmin@10.0.0.$NODE 'DISPLAY=:0 feh --fullscreen --hide-pointer --auto-zoom --no-menus /home/radmin/cluster_result.png >/tmp/feh.log 2>&1 &' </dev/null >/dev/null 2>&1 &
    done
    sleep 2

    echo
    echo "========================================="
    echo "Demo Complete! All screens showing result."
    echo "========================================="
else
    echo "Error: Result image not found"
fi