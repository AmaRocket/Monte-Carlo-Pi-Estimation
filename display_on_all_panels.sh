#!/bin/bash
# Display image across all 4 panels (or specific panel)
# Usage: ./display_on_panels.sh <image_path> [panel_number]
# If panel_number not specified, displays on all 4 panels

IMAGE=$1
PANEL=$2

if [ -z "$IMAGE" ]; then
    echo "Usage: $0 <image_path> [panel_number]"
    echo "Example: $0 result.png      # All panels"
    echo "Example: $0 result.png 1    # Only panel 1"
    exit 1
fi

if [ ! -f "$IMAGE" ]; then
    echo "Error: Image $IMAGE not found"
    exit 1
fi

display_on_single_panel() {
    local IMAGE=$1
    local PANEL=$2

    PANEL_FILE="/export/infoTag2025/panel${PANEL}"
    if [ ! -f "$PANEL_FILE" ]; then
        echo "Error: Panel file $PANEL_FILE not found"
        return 1
    fi

    echo "Panel $PANEL: Splitting image..."

    # Create tiles directory
    TILES_DIR="/tmp/panel${PANEL}_tiles"
    rm -rf "$TILES_DIR"
    mkdir -p "$TILES_DIR"

    # Split image using Python
    python3 << PYEND
from PIL import Image

img = Image.open("$IMAGE")
width, height = img.size
tile_width = width // 4
tile_height = height // 4

tile_num = 0
for row in range(4):
    for col in range(4):
        left = col * tile_width
        top = row * tile_height
        right = left + tile_width
        bottom = top + tile_height

        tile = img.crop((left, top, right, bottom))
        tile.save(f"$TILES_DIR/tile_{tile_num}.png")
        tile_num += 1
PYEND

    echo "Panel $PANEL: Distributing tiles..."

    # Read panel layout and distribute tiles
    mapfile -t ROWS < "$PANEL_FILE"

    tile_num=0
    for row in {0..3}; do
        IFS=' ' read -ra NODES <<< "${ROWS[$row]}"
        for col in {0..3}; do
            node=${NODES[$col]}
            tile_file="$TILES_DIR/tile_${tile_num}.png"

            if [ -f "$tile_file" ]; then
                scp -q "$tile_file" radmin@${node}:/tmp/my_tile.png &
            fi

            ((tile_num++))
        done
    done
    wait

    echo "Panel $PANEL: Displaying..."
    for row in {0..3}; do
        IFS=' ' read -ra NODES <<< "${ROWS[$row]}"
        for node in "${NODES[@]}"; do
            ssh radmin@${node} 'pkill feh; DISPLAY=:0 feh --fullscreen --hide-pointer --auto-zoom --no-menus /tmp/my_tile.png >/tmp/feh.log 2>&1 &' </dev/null >/dev/null 2>&1 &
        done
    done
    wait

    echo "Panel $PANEL: Complete!"
}

echo "========================================="
echo "Monte Carlo Pi - Panel Display"
echo "========================================="

if [ -z "$PANEL" ]; then
    # Display on all 4 panels
    echo "Displaying on all 4 panels..."
    echo
    for p in 1 2 3 4; do
        display_on_single_panel "$IMAGE" $p
    done
else
    # Display on specific panel
    echo "Displaying on Panel $PANEL..."
    echo
    display_on_single_panel "$IMAGE" $PANEL
fi

echo
echo "========================================="
echo "Display complete!"
echo "========================================="