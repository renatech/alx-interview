#!/usr/bin/python3
"""
Log parsing
"""

import sys
import signal

# Initialize counters and storage
total_size = 0
status_codes_count = {200: 0, 301: 0, 400: 0, 401: 0, 403: 0, 404: 0, 405: 0, 500: 0}
line_count = 0

def print_stats():
    """Print the accumulated statistics."""
    global total_size, status_codes_count
    print(f"Total file size: {total_size}")
    for code in sorted(status_codes_count.keys()):
        if status_codes_count[code] > 0:
            print(f"{code}: {status_codes_count[code]}")

def signal_handler(sig, frame):
    """Handle the keyboard interrupt signal to print stats and exit."""
    print_stats()
    sys.exit(0)

# Register the signal handler for keyboard interruption
signal.signal(signal.SIGINT, signal_handler)

try:
    for line in sys.stdin:
        # Split the line by spaces to parse it
        parts = line.split()

        # Validate the line format
        if len(parts) < 7:
            continue

        ip_address = parts[0]
        date = parts[3] + " " + parts[4]
        request = parts[5] + " " + parts[6] + " " + parts[7]
        status_code = parts[-2]
        file_size = parts[-1]

        # Validate the request and status code
        if request.startswith('"GET') and request.endswith('HTTP/1.1"'):
            try:
                status_code = int(status_code)
                file_size = int(file_size)

                # Update the total file size
                total_size += file_size

                # Update the status code count
                if status_code in status_codes_count:
                    status_codes_count[status_code] += 1

                # Increment the line count
                line_count += 1

                # Print stats every 10 lines
                if line_count % 10 == 0:
                    print_stats()
            except ValueError:
                # If conversion to int fails, skip the line
                continue

except KeyboardInterrupt:
    # Handle keyboard interruption explicitly
    print_stats()
    sys.exit(0)
