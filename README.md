# Monte-Carlo-Pi-Estimation
Monte Carlo Pi Estimation - MVP Version Estimates Pi by randomly sampling points in a unit square
Current version tested on 64 Raspberry Pi worker Cluster

# Main Files:

1. run_cluster_demo.sh - Main runner script
◦  Clears all screens and old images
◦  Runs MPI computation across all 64 nodes (256 processes)
◦  Fetches result from rank 0 node
◦  Distributes and displays result on all screens
2. monte_carlo_summary.py - Python visualization script
◦  Performs Monte Carlo Pi calculation using MPI
◦  Creates single summary visualization with:
▪  Large graph on left (75% width)
▪  Performance box on top right (25% width, 50% height)
▪  Cluster Results box on bottom right (25% width, 50% height)
◦  Saves to /home/radmin/monte_carlo_demo/cluster_result.png

# Run the script:

Test with different sample sizes 

/run_cluster_demo.sh 10000000


![img.png](img.png)


# Install OpenMPI and Python bindings
sudo apt-get install openmpi-bin libopenmpi-dev python3-pip
pip3 install mpi4py

