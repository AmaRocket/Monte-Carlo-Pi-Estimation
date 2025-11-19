#!/bin/bash

# Clear all screens, images, and Python cache on all nodes
echo "Clearing all screens and old images..."
for NODE in {101..164}; do
    ssh radmin@10.0.0.$NODE "pkill -9 feh; rm -rf /home/radmin/*.png /home/radmin/monte_carlo_demo/*.png /tmp/*.png /export/infoTag2025/updated_scripts/applications/monte_carlo_pi/__pycache__" 2>/dev/null &
done
wait
echo "All caches cleared."
echo