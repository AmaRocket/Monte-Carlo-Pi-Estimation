#!/bin/bash

## Clear/blank all screens on worker nodes

echo "Clearing screens on all worker nodes..."
echo "========================================"

WORKERS=($(seq -f "10.0.0.%g" 101 164))
SUCCESS=0
FAILED=0

for WORKER in "${WORKERS[@]}"; do
    WORKER_NUM=$(echo $WORKER | cut -d. -f4)
    WORKER_NAME="micro-cluster-worker$(printf "%02d" $((WORKER_NUM - 100)))"

    echo -n "Clearing $WORKER_NAME ($WORKER)... "

    # Check if node is reachable
    if ! ping -c 1 -W 2 $WORKER > /dev/null 2>&1; then
        echo "[SKIP] Not reachable"
        continue
    fi

    # Kill fbi and clear framebuffer
    ssh -o ConnectTimeout=5 radmin@$WORKER << 'REMOTE_SCRIPT' >/dev/null 2>&1
        # Kill any running fbi/X processes
        sudo pkill fbi
        sudo pkill Xorg
        sudo pkill xinit

        # Clear the framebuffer (set to black)
        if [ -e /dev/fb0 ]; then
            sudo dd if=/dev/zero of=/dev/fb0 bs=1M count=8 2>/dev/null || true
        fi
REMOTE_SCRIPT

    if [ $? -eq 0 ]; then
        echo "[OK]"
        ((SUCCESS++))
    else
        echo "[FAIL]"
        ((FAILED++))
    fi
done

echo "========================================"
echo "Summary:"
echo "  Cleared: $SUCCESS nodes"
echo "  Failed:  $FAILED nodes"
echo "========================================"