#!/usr/bin/env python3
from playwright.sync_api import sync_playwright
import os

def take_screenshot():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    html_path = os.path.join(script_dir, 'card_v1.html')
    output_path = os.path.join(script_dir, 'outputs', 'output_v1.png')

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={'width': 720, 'height': 720})

        page.goto(f'file://{html_path}')
        page.wait_for_timeout(1000)  # Wait for fonts to load

        page.screenshot(path=output_path, full_page=False)

        print(f'Screenshot saved to {output_path}')
        browser.close()

if __name__ == '__main__':
    take_screenshot()
