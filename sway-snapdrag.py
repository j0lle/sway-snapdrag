import os
import subprocess
import json
import time
from typing import List, Optional, Dict, Any

class ScreenshotManager:
    def __init__(self, save_dir: str):
        self.save_dir = os.path.expanduser(save_dir)
        os.makedirs(self.save_dir, exist_ok=True)

    def fetch_sway_tree(self) -> Optional[Dict[str, Any]]:
        try:
            swaymsg_output = subprocess.check_output(['swaymsg', '-t', 'get_tree'], universal_newlines=True)
            return json.loads(swaymsg_output)
        except Exception as e:
            print("Error fetching sway tree:", e)
            return None

    def collect_window_data(self, node: Dict[str, Any]) -> List[str]:
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
            windows.extend(self.collect_window_data(child))
        return windows

    def run_slurp(self, window_data: str) -> Optional[str]:
        try:
            slurp_proc = subprocess.Popen(['slurp'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, universal_newlines=True)
            selected_region, _ = slurp_proc.communicate(input=window_data)
            return selected_region.strip()
        except Exception as e:
            print("Error running slurp:", e)
            return None

    def find_window_at_point(self, node: Dict[str, Any], x: int, y: int) -> Optional[Dict[str, Any]]:
        if node.get('type') == 'con' and 'pid' in node:
            rect = node.get('rect', {})
            x0, y0 = rect.get('x', 0), rect.get('y', 0)
            width, height = rect.get('width', 0), rect.get('height', 0)
            if x0 <= x <= x0 + width and y0 <= y <= y0 + height:
                return node
        for child in node.get('nodes', []) + node.get('floating_nodes', []):
            result = self.find_window_at_point(child, x, y)
            if result:
                return result
        return None

    def take_screenshot(self, region: str, filename: str):
        try:
            filepath = os.path.join(self.save_dir, filename)
            subprocess.run(['grim', '-g', region, filepath])
            with open(filepath, 'rb') as f:
                subprocess.run(['wl-copy'], stdin=f)
            subprocess.run(['notify-send', 'Screenshot saved and copied to clipboard', filepath])
        except Exception as e:
            print("Error taking screenshot:", e)

    def sanitize_app_name(self, app_name: str) -> str:
        return app_name.strip().replace('/', '_').replace(' ', '_').lstrip('_')

    def create_filename(self, app_name: str) -> str:
        safe_name = self.sanitize_app_name(app_name)
        return f"{safe_name}-{time.strftime('%Y%m%d-%H%M%S')}.png"

    def process_selected_region(self, sway_tree: Dict[str, Any], selected_region: str, window_data_list: List[str]):
        matched_window = next((line for line in window_data_list if line.startswith(selected_region)), None)

        if matched_window:
            print("Matched window selection.")
            parts = matched_window.split()
            region, app_name = f"{parts[0]} {parts[1]}", ' '.join(parts[2:])
        else:
            print("Drag selection detected.")
            x, y, w, h = self.parse_region(selected_region)
            window_node = self.find_window_at_point(sway_tree, x, y)
            app_name = (
                window_node.get('app_id')
                or window_node.get('name')
                or window_node.get('window_properties', {}).get('class')
                or 'screenshot'
            ) if window_node else 'screenshot'
            region = selected_region

        filename = self.create_filename(app_name)
        self.take_screenshot(region, filename)

    @staticmethod
    def parse_region(region: str) -> (int, int, int, int):
        x_y, w_h = region.split()
        x, y = map(int, x_y.split(','))
        w, h = map(int, w_h.split('x'))
        return x, y, w, h


def main():
    manager = ScreenshotManager(save_dir="~/Pictures/Screenshots")
    sway_tree = manager.fetch_sway_tree()

    if not sway_tree:
        return

    window_data_list = manager.collect_window_data(sway_tree)
    window_data = '\n'.join(window_data_list)
    selected_region = manager.run_slurp(window_data)

    if not selected_region:
        print("Selection cancelled.")
        return

    manager.process_selected_region(sway_tree, selected_region, window_data_list)


if __name__ == '__main__':
    main()
