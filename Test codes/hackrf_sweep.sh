#!/bin/bash
SAMPLE_DURATION=60  # Set duration to collect data (adjust if needed)

read -p "Enter filename: " FILENAME
FILENAME="$FILENAME.csv"
echo "Saving data to: $FILENAME"

if [ ! -f "$FILENAME" ]; then
    echo "Starting HackRF sweep for $SAMPLE_DURATION seconds..."
    hackrf_sweep -f 2400:2500 -N 60000000 -w 600000 -r "$FILENAME"
    echo "Sweep complete. Data saved."
else
    echo "File already exists!"
fi
