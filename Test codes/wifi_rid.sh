#!/bin/bash
echo "Starting Wi-Fi Remote ID Sniffing..."
trap 'echo "Stopping HackRF..."; sudo killall hackrf_transfer; exit' SIGINT

hackrf_transfer -r wifi_scan.raw -f 2437000000 -s 20000000 -l 40 -g 40 &
sleep 10  # Capture for 10 seconds
sudo killall hackrf_transfer  # Ensure HackRF stops
tshark -r wifi_scan.raw -w wifi_scan.pcap
echo "Wi-Fi Remote ID Captured!"
