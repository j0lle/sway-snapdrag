#!/usr/bin/env python3

import os
import subprocess
import json
import time

def main():
    DIR = os.path.expanduser("~/Pictures/Screenshots")
    os.makedirs(DIR, exist_ok=True)

    # Fetch window data: position, size, and app name
    try:
        swaymsg_output = subprocess.check_output(['swaymsg', '-t', 'get_tree'], universal_newlines=True)
        sway_tree = json.loads(swaymsg_output)
    except Exception as e:
        print("Error fetching sway tree:", e)
        return

    # Helper function to traverse the tree and collect window data
    def collect_window_data(node):
        windows = []
        if 'pid' in node and node.get('visible', False):
            rect = node.get('rect', {})
            window_rect = node.get('window_rect', {})
            x = rect.get('x', 0) + window_rect.get('x', 0)
            y = rect.get('y', 0) + window_rect.get('y', 0)
            width = window_rect.get('width', 0)
            height = window_rect.get('height', 0)
            app_id = node.get('app_id') or node.get('name', 'unknown')
            windows.append(f"{x},{y} {width}x{height} {app_id}")
        for child in node.get('nodes', []) + node.get('floating_nodes', []):
            windows.extend(collect_window_data(child))
        return windows

    WINDOW_DATA_LIST = collect_window_data(sway_tree)
    WINDOW_DATA = '\n'.join(WINDOW_DATA_LIST)

    # Run slurp with the WINDOW_DATA as input
    try:
        slurp_proc = subprocess.Popen(['slurp'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, universal_newlines=True)
        SELECTED_REGION, _ = slurp_proc.communicate(input=WINDOW_DATA)
        SELECTED_REGION = SELECTED_REGION.strip()
    except Exception as e:
        print("Error running slurp:", e)
        return

    print(f"Selected region: {SELECTED_REGION}")

    if not SELECTED_REGION:
        print("Selection cancelled.")
        return

    # Try to find a window that matches the selected region exactly (window selection)
    MATCHED_WINDOW = ''
    for line in WINDOW_DATA_LIST:
        if line.startswith(SELECTED_REGION):
            MATCHED_WINDOW = line
            break

    if MATCHED_WINDOW:
        print("Entering window selection section")
        # Extract REGION and APP_NAME
        parts = MATCHED_WINDOW.split()
        REGION = f"{parts[0]} {parts[1]}"
        APP_NAME = ' '.join(parts[2:])
        SAFE_APP_NAME = APP_NAME.strip().replace('/', '_').replace(' ', '_').lstrip('_')
        FILENAME = f"{SAFE_APP_NAME}-{time.strftime('%Y%m%d-%H%M%S')}.png"
        FILENAME_PATH = os.path.join(DIR, FILENAME)

        # Take screenshot and copy to clipboard
        try:
            subprocess.run(['grim', '-g', REGION, FILENAME_PATH])
            with open(FILENAME_PATH, 'rb') as f:
                subprocess.run(['wl-copy'], stdin=f)
            subprocess.run(['notify-send', 'Screenshot saved and copied to clipboard', FILENAME_PATH])
        except Exception as e:
            print("Error taking screenshot:", e)
            return
    else:
        print("Entering drag selection section")
        # Parse SELECTED_REGION to get x, y, width, and height
        x_y, w_h = SELECTED_REGION.split()
        x_str, y_str = x_y.split(',')
        w_str, h_str = w_h.split('x')
        x = int(x_str)
        y = int(y_str)
        w = int(w_str)
        h = int(h_str)

        print(f"Parsed Coordinates:\nStarting x: {x}\nStarting y: {y}\nWidth: {w}\nHeight: {h}")

        # Find the window at the starting point
        # Helper function to recursively find the window under the starting point
        def find_window_at_point(node, x, y):
            if node.get('type') == 'con' and 'pid' in node:
                rect = node.get('rect', {})
                x0 = rect.get('x', 0)
                y0 = rect.get('y', 0)
                width = rect.get('width', 0)
                height = rect.get('height', 0)
                if x0 <= x <= x0 + width and y0 <= y <= y0 + height:
                    return node
            for child in node.get('nodes', []) + node.get('floating_nodes', []):
                result = find_window_at_point(child, x, y)
                if result:
                    return result
            return None

        window_node = find_window_at_point(sway_tree, x, y)

        if window_node:
            ACTIVE_WINDOW_NAME = window_node.get('app_id') or window_node.get('name') or window_node.get('window_properties', {}).get('class') or 'unknown'
            print(f"Window at starting point of selection: {ACTIVE_WINDOW_NAME}")
        else:
            ACTIVE_WINDOW_NAME = 'screenshot'
            print("No window found at starting point. Using default name 'screenshot'.")

        SAFE_APP_NAME = ACTIVE_WINDOW_NAME.strip().replace('/', '_').replace(' ', '_').lstrip('_')
        FILENAME = f"{SAFE_APP_NAME}-{time.strftime('%Y%m%d-%H%M%S')}.png"
        FILENAME_PATH = os.path.join(DIR, FILENAME)

        # Take screenshot and copy to clipboard
        try:
            subprocess.run(['grim', '-g', SELECTED_REGION, FILENAME_PATH])
            with open(FILENAME_PATH, 'rb') as f:
                subprocess.run(['wl-copy'], stdin=f)
            subprocess.run(['notify-send', 'Screenshot saved and copied to clipboard', FILENAME_PATH])
        except Exception as e:
            print("Error taking screenshot:", e)
            return

if __name__ == '__main__':
    main()
