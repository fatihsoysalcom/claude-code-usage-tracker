import time
import re
from collections import deque

# Simulate log file path
LOG_FILE = 'claude_usage.log'

# Define the sliding window size (e.g., 5 hours in seconds)
WINDOW_SECONDS = 5 * 60 * 60

# Store timestamps of 'usage' events
usage_timestamps = deque()

def simulate_log_entry(event_type):
    """Simulates writing an entry to the log file."""
    timestamp = int(time.time())
    with open(LOG_FILE, 'a') as f:
        f.write(f"{timestamp} - {event_type}\n")

def parse_log_for_usage(log_line):
    """Parses a log line to check if it's a 'usage' event."""
    # Simple regex to find timestamps and event types
    match = re.match(r'(\d+) - (.*)', log_line)
    if match:
        timestamp, event = match.groups()
        # Assume 'usage' is indicated by a specific event string
        if 'usage' in event.lower():
            return int(timestamp)
    return None

def update_usage_tracker():
    """Reads the log file, updates usage timestamps, and calculates current usage."""
    global usage_timestamps

    current_time = time.time()

    # Read new entries from the log file
    try:
        with open(LOG_FILE, 'r') as f:
            # In a real scenario, you'd likely read only new lines since last check
            # For simplicity, we re-read and filter
            all_lines = f.readlines()
    except FileNotFoundError:
        all_lines = []

    # Rebuild timestamps from scratch for simplicity in this example
    # A more efficient approach would be to only process new lines
    current_usage_timestamps = []
    for line in all_lines:
        ts = parse_log_for_usage(line)
        if ts:
            current_usage_timestamps.append(ts)

    # Filter timestamps within the sliding window
    valid_timestamps = [ts for ts in current_usage_timestamps if current_time - ts <= WINDOW_SECONDS]

    usage_timestamps = deque(valid_timestamps)

    return len(usage_timestamps)

def display_usage_status():
    """Displays the current usage status based on the tracker."""
    current_usage_count = update_usage_tracker()
    print(f"\n--- Claude Code Usage Status ---")
    print(f"Window: {WINDOW_SECONDS // 3600} hours")
    print(f"Active usage events in window: {current_usage_count}")
    # This count can be used to estimate remaining usage based on known limits
    # For example, if 100 events are allowed per 5 hours, you can calculate percentage
    print(f"-------------------------------")

if __name__ == "__main__":
    # Clean up old log file for a fresh start in this example
    try:
        with open(LOG_FILE, 'w') as f:
            pass
    except IOError:
        pass

    print(f"Simulating Claude Code usage. Log file: {LOG_FILE}")
    print(f"Monitoring a {WINDOW_SECONDS // 3600}-hour window.")

    # Simulate some initial usage
    simulate_log_entry("User started coding session")
    time.sleep(1)
    simulate_log_entry("Claude Code provided suggestion")
    time.sleep(1)
    simulate_log_entry("Claude Code generated code snippet")

    display_usage_status()

    # Simulate more usage over time
    print("\nSimulating more usage over the next few seconds...")
    for _ in range(5):
        time.sleep(2)
        simulate_log_entry("Claude Code assisted with refactoring")
        display_usage_status()

    # Simulate a long pause to show window effect
    print(f"\nPausing for {WINDOW_SECONDS // 2} seconds to demonstrate window sliding...")
    time.sleep(WINDOW_SECONDS // 2)

    # Simulate more usage after the pause
    print("\nSimulating usage after a long pause...")
    simulate_log_entry("Claude Code helped debug")
    display_usage_status()

    print("\nSimulation finished.")
