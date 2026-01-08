#!/usr/bin/env python3
"""
Extract and convert Moodle backup (.mbz) to markdown.
.mbz files are gzipped tar archives.
"""

import gzip
import tarfile
import xml.etree.ElementTree as ET
import os
import sys
from pathlib import Path

def extract_mbz(mbz_path, extract_dir):
    """Extract .mbz (gzipped tar) file to directory."""
    print(f"Extracting {mbz_path}...")
    
    # .mbz files are gzipped tar archives
    with gzip.open(mbz_path, 'rb') as gz_file:
        with tarfile.open(fileobj=gz_file, mode='r') as tar:
            tar.extractall(extract_dir)
    
    print(f"Extracted to {extract_dir}")

def find_book_xml(extract_dir):
    """Find book activity XML files in the extracted backup."""
    book_files = []
    
    # Look for moodle_backup.xml first
    backup_xml = Path(extract_dir) / "moodle_backup.xml"
    if backup_xml.exists():
        print(f"Found {backup_xml}")
        tree = ET.parse(backup_xml)
        root = tree.getroot()
        
        # Look for book activities
        for activity in root.findall(".//activity[@moduleid='book']"):
            activity_id = activity.get('moduleid')
            print(f"Found book activity: {activity_id}")
    
    # Also search for book.xml files directly
    for book_xml in Path(extract_dir).rglob("book.xml"):
        print(f"Found book.xml at: {book_xml}")
        book_files.append(book_xml)
    
    return book_files

def main():
    mbz_file = "backup-moodle2-activity-2600518-book2600518-20260108-1341-nu.mbz"
    extract_dir = "temp_extract"
    
    if not os.path.exists(mbz_file):
        print(f"Error: {mbz_file} not found")
        sys.exit(1)
    
    # Create extraction directory
    os.makedirs(extract_dir, exist_ok=True)
    
    # Extract the backup
    extract_mbz(mbz_file, extract_dir)
    
    # Find book XML files
    book_files = find_book_xml(extract_dir)
    
    print(f"\nFound {len(book_files)} book XML file(s)")
    
    # List directory structure
    print("\nDirectory structure:")
    for root, dirs, files in os.walk(extract_dir):
        level = root.replace(extract_dir, '').count(os.sep)
        indent = ' ' * 2 * level
        print(f"{indent}{os.path.basename(root)}/")
        subindent = ' ' * 2 * (level + 1)
        for file in files[:10]:  # Show first 10 files
            print(f"{subindent}{file}")

if __name__ == "__main__":
    main()

