#!/usr/bin/env python3
"""
HTML to Image Converter using Playwright

Usage:
    python3 html_to_image.py <html_file> <output_image>

Example:
    python3 html_to_image.py ./example2/outputs/output.html ./example2/outputs/output_v1.png
"""

import sys
import os
from pathlib import Path
from playwright.sync_api import sync_playwright


def html_to_image(html_path: str, output_path: str):
    """Convert HTML file to PNG image using Playwright"""
    
    # Convert to absolute paths
    html_path = Path(html_path).resolve()
    output_path = Path(output_path).resolve()
    
    # Ensure HTML file exists
    if not html_path.exists():
        print(f"Error: HTML file not found: {html_path}")
        sys.exit(1)
    
    # Create output directory if it doesn't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Convert HTML to image
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        
        # Load HTML file
        page.goto(f"file://{html_path}")
        
        # Wait for page to load
        page.wait_for_load_state("networkidle")
        
        # Take screenshot
        page.screenshot(path=str(output_path), full_page=True)
        
        browser.close()
    
    print(f"✓ Screenshot saved to: {output_path}")


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    
    html_file = sys.argv[1]
    output_file = sys.argv[2]
    
    html_to_image(html_file, output_file)


if __name__ == "__main__":
    main()
