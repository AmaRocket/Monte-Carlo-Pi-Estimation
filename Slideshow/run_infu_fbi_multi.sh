#!/bin/bash

## Display images using fbi (framebuffer) on all nodes defined in IMAGE_MAP
### TO RUN: /tmp/run_info_fbi_all.sh

IMAGE_BASE="/export/applications/images/"

# IP to image mapping
declare -A IMAGE_MAP=(
    ["10.0.0.116"]="cluster_info_split/Slide1.png"
    ["10.0.0.115"]="cluster_info_split/Slide2.png"
    ["10.0.0.114"]="cluster_info_split/Slide3.png"
    ["10.0.0.113"]="cluster_info_split/Slide4.png"
    ["10.0.0.112"]="cluster_info_split/Slide5.png"
    ["10.0.0.111"]="cluster_info_split/Slide6.png"
    ["10.0.0.110"]="cluster_info_split/Slide7.png"
    ["10.0.0.109"]="cluster_info_split/Slide8.png"
    ["10.0.0.108"]="cluster_info_split/Slide9.png"
    ["10.0.0.107"]="qr_codes/qr_dmi_bachelor.png"
    ["10.0.0.106"]="cluster_info_split/Slide10.png"
    ["10.0.0.105"]="qr_codes/qr_dmi.png"
    ["10.0.0.104"]="cluster_info_split/Slide11.png"
    ["10.0.0.103"]="qr_codes/qr_hpc_group.png"
    ["10.0.0.102"]="cluster_info_split/Slide12_insta.png"
    ["10.0.0.101"]="qr_codes/qr_hpc_linkedin.png"
    ["10.0.0.117"]="logos/unibas.png"
    ["10.0.0.119"]="logos/unibas.png"
    ["10.0.0.122"]="logos/unibas.png"
    ["10.0.0.124"]="logos/unibas.png"
    ["10.0.0.125"]="logos/unibas.png"
    ["10.0.0.127"]="logos/unibas.png"
    ["10.0.0.130"]="logos/unibas.png"
    ["10.0.0.132"]="logos/unibas.png"
    ["10.0.0.118"]="logos/hpc.png"
    ["10.0.0.120"]="logos/hpc.png"
    ["10.0.0.121"]="logos/hpc.png"
    ["10.0.0.123"]="logos/hpc.png"
    ["10.0.0.126"]="logos/hpc.png"
    ["10.0.0.128"]="logos/hpc.png"
    ["10.0.0.129"]="logos/hpc.png"
    ["10.0.0.131"]="logos/hpc.png"
    ["10.0.0.133"]="cluster_info_split/Slide1.png"
    ["10.0.0.134"]="cluster_info_split/Slide2.png"
    ["10.0.0.135"]="cluster_info_split/Slide3.png"
    ["10.0.0.136"]="cluster_info_split/Slide4.png"
    ["10.0.0.137"]="cluster_info_split/Slide5.png"
    ["10.0.0.138"]="cluster_info_split/Slide6.png"
    ["10.0.0.139"]="cluster_info_split/Slide7.png"
    ["10.0.0.140"]="cluster_info_split/Slide8.png"
    ["10.0.0.141"]="cluster_info_split/Slide9.png"
    ["10.0.0.142"]="qr_codes/qr_dmi_bachelor.png"
    ["10.0.0.143"]="cluster_info_split/Slide10.png"
    ["10.0.0.144"]="qr_codes/qr_dmi.png"
    ["10.0.0.145"]="cluster_info_split/Slide11.png"
    ["10.0.0.146"]="qr_codes/qr_hpc_group.png"
    ["10.0.0.147"]="cluster_info_split/Slide12.png"
    ["10.0.0.148"]="qr_codes/qr_hpc_linkedin.png"
    ["10.0.0.161"]="logos/unibas.png"
    ["10.0.0.163"]="logos/unibas.png"
    ["10.0.0.158"]="logos/unibas.png"
    ["10.0.0.160"]="logos/unibas.png"
    ["10.0.0.155"]="logos/unibas.png"
    ["10.0.0.153"]="logos/unibas.png"
    ["10.0.0.150"]="logos/unibas.png"
    ["10.0.0.152"]="logos/unibas.png"
    ["10.0.0.162"]="logos/hpc.png"
    ["10.0.0.164"]="logos/hpc.png"
    ["10.0.0.157"]="logos/hpc.png"
    ["10.0.0.159"]="logos/hpc.png"
    ["10.0.0.156"]="logos/hpc.png"
    ["10.0.0.154"]="logos/hpc.png"
    ["10.0.0.149"]="logos/hpc.png"
    ["10.0.0.151"]="logos/hpc.png"

)

echo "Starting fbi slideshow on all nodes..."
echo "======================================"

SUCCESS=0
SKIPPED=0

# Process all nodes in IMAGE_MAP
for node in "${!IMAGE_MAP[@]}"; do
    image_file="${IMAGE_MAP[$node]}"
    image_path="${IMAGE_BASE}${image_file}"

    # Check if node is reachable
    if ! ping -c 1 -W 2 $node > /dev/null 2>&1; then
        echo "  [SKIP] $node - not reachable"
        ((SKIPPED++))
        continue
    fi

    # Kill any existing fbi/X processes
    ssh radmin@$node "sudo pkill fbi; sudo pkill Xorg; sudo pkill xinit" 2>/dev/null

    # Display the image using fbi - use setsid to properly detach
    ssh radmin@$node "sudo setsid fbi -T 1 -d /dev/fb0 -noverbose -a $image_path >/tmp/fbi_$node.log 2>&1 &" 2>/dev/null

    echo "  ✓ $node -> $image_file"
    ((SUCCESS++))
done

echo "======================================"
echo "Summary:"
echo "  Started: $SUCCESS nodes"
echo "  Skipped: $SKIPPED nodes"
echo "======================================"