#!/usr/bin/env python3
"""
Convert Moodle book backup to markdown format.
"""

import gzip
import tarfile
import xml.etree.ElementTree as ET
import os
import sys
import html
import re
from pathlib import Path
from html.parser import HTMLParser
from html import unescape

class HTMLToMarkdownConverter(HTMLParser):
    """Simple HTML to Markdown converter."""
    
    def __init__(self):
        super().__init__()
        self.markdown = []
        self.current_tag = None
        self.list_stack = []
        self.in_code = False
        self.in_pre = False
        self.link_text = None
        self.link_url = None
        
    def handle_starttag(self, tag, attrs):
        self.current_tag = tag
        attrs_dict = dict(attrs)
        
        if tag == 'h1':
            self.markdown.append('\n# ')
        elif tag == 'h2':
            self.markdown.append('\n## ')
        elif tag == 'h3':
            self.markdown.append('\n### ')
        elif tag == 'h4':
            self.markdown.append('\n#### ')
        elif tag == 'h5':
            self.markdown.append('\n##### ')
        elif tag == 'h6':
            self.markdown.append('\n###### ')
        elif tag == 'p':
            # Only add newline if not in a list
            if not self.list_stack:
                if self.markdown and not self.markdown[-1].endswith('\n\n'):
                    self.markdown.append('\n\n')
        elif tag == 'br':
            self.markdown.append('\n')
        elif tag == 'strong' or tag == 'b':
            self.markdown.append('**')
        elif tag == 'em' or tag == 'i':
            self.markdown.append('*')
        elif tag == 'code':
            self.markdown.append('`')
            self.in_code = True
        elif tag == 'pre':
            self.in_pre = True
            self.markdown.append('\n```\n')
        elif tag == 'ul':
            self.list_stack.append('ul')
        elif tag == 'ol':
            self.list_stack.append('ol')
            self.list_counter = 1
        elif tag == 'li':
            indent = '  ' * (len(self.list_stack) - 1)
            if self.list_stack and self.list_stack[-1] == 'ol':
                self.markdown.append(f'\n{indent}1. ')
            else:
                self.markdown.append(f'\n{indent}- ')
        elif tag == 'a':
            self.link_url = attrs_dict.get('href', '')
            self.link_text = []
        elif tag == 'img':
            src = attrs_dict.get('src', '')
            alt = attrs_dict.get('alt', '')
            # Preserve Moodle image references
            self.markdown.append(f'![{alt}]({src})')
        elif tag == 'hr':
            self.markdown.append('\n---\n')
            
    def handle_endtag(self, tag):
        if tag == 'h1' or tag == 'h2' or tag == 'h3' or tag == 'h4' or tag == 'h5' or tag == 'h6':
            self.markdown.append('\n')
        elif tag == 'p':
            self.markdown.append('\n')
        elif tag == 'strong' or tag == 'b':
            self.markdown.append('**')
        elif tag == 'em' or tag == 'i':
            self.markdown.append('*')
        elif tag == 'code':
            self.markdown.append('`')
            self.in_code = False
        elif tag == 'pre':
            self.markdown.append('\n```\n')
            self.in_pre = False
        elif tag == 'ul' or tag == 'ol':
            if self.list_stack:
                self.list_stack.pop()
            self.markdown.append('\n')
        elif tag == 'a':
            if self.link_url and self.link_text:
                text = ''.join(self.link_text)
                self.markdown.append(f'[{text}]({self.link_url})')
            self.link_text = None
            self.link_url = None
            
        self.current_tag = None
        
    def handle_data(self, data):
        if self.in_pre and not self.in_code:
            # Preserve code block content as-is
            self.markdown.append(data)
        elif self.current_tag == 'a':
            if self.link_text is not None:
                self.link_text.append(data)
        else:
            # Clean up whitespace but preserve structure
            if not self.in_code:
                # For list items, preserve some whitespace
                if self.current_tag == 'li' or (self.list_stack and self.current_tag == 'p'):
                    # In lists, preserve single spaces but collapse multiple
                    data = ' '.join(data.split())
                else:
                    data = data.strip()
                if data:
                    # Add space before if needed (for inline elements)
                    if self.markdown and self.markdown[-1] not in [' ', '\n', '-', '1.', '*', '**', '`']:
                        if not self.list_stack or self.current_tag not in ['li', 'p']:
                            self.markdown.append(' ')
                    self.markdown.append(data)
            else:
                self.markdown.append(data)
    
    def get_markdown(self):
        result = ''.join(self.markdown)
        # Clean up excessive newlines
        result = re.sub(r'\n{3,}', '\n\n', result)
        # Fix list items with empty content
        result = re.sub(r'^(\s*[-*]|\s*\d+\.)\s*\n\n', r'\1 ', result, flags=re.MULTILINE)
        # Remove spaces before list markers
        result = re.sub(r'\n\s+(-|\d+\.)', r'\n\1', result)
        # Clean up multiple spaces
        result = re.sub(r' {2,}', ' ', result)
        return result.strip()

def html_to_markdown(html_content):
    """Convert HTML content to markdown."""
    # First unescape HTML entities
    html_content = unescape(html_content)
    
    # Use our converter
    converter = HTMLToMarkdownConverter()
    converter.feed(html_content)
    return converter.get_markdown()

def extract_and_convert(mbz_file, output_file):
    """Extract Moodle backup and convert to markdown."""
    
    extract_dir = "temp_extract"
    
    # Extract the backup
    print(f"Extracting {mbz_file}...")
    os.makedirs(extract_dir, exist_ok=True)
    
    with gzip.open(mbz_file, 'rb') as gz_file:
        with tarfile.open(fileobj=gz_file, mode='r') as tar:
            tar.extractall(extract_dir)
    
    # Find book XML
    book_xml = Path(extract_dir) / "activities" / "book_2600518" / "book.xml"
    
    if not book_xml.exists():
        print(f"Error: Book XML not found at {book_xml}")
        sys.exit(1)
    
    # Parse book XML
    print(f"Parsing {book_xml}...")
    tree = ET.parse(book_xml)
    root = tree.getroot()
    
    # Get book name
    book_name = root.find('.//name').text if root.find('.//name') is not None else "Learning Material"
    
    # Extract chapters
    chapters = []
    for chapter in root.findall('.//chapter'):
        pagenum = int(chapter.find('pagenum').text) if chapter.find('pagenum') is not None else 999
        subchapter = int(chapter.find('subchapter').text) if chapter.find('subchapter') is not None else 0
        title = chapter.find('title').text if chapter.find('title') is not None else "Untitled"
        content = chapter.find('content').text if chapter.find('content') is not None else ""
        hidden = int(chapter.find('hidden').text) if chapter.find('hidden') is not None else 0
        
        if not hidden:  # Skip hidden chapters
            chapters.append({
                'pagenum': pagenum,
                'subchapter': subchapter,
                'title': title,
                'content': content
            })
    
    # Sort chapters by page number
    chapters.sort(key=lambda x: (x['pagenum'], x['subchapter']))
    
    print(f"Found {len(chapters)} chapters")
    
    # Convert to markdown
    markdown_content = [f"# {book_name}\n"]
    
    for i, chapter in enumerate(chapters):
        # Determine heading level based on subchapter
        heading_level = '##' if chapter['subchapter'] == 0 else '###'
        markdown_content.append(f"\n{heading_level} {chapter['title']}\n")
        
        # Convert HTML content to markdown
        if chapter['content']:
            md_content = html_to_markdown(chapter['content'])
            markdown_content.append(md_content)
            markdown_content.append('\n')
    
    # Write output file
    final_markdown = ''.join(markdown_content)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(final_markdown)
    
    print(f"Markdown file created: {output_file}")
    print(f"Total size: {len(final_markdown)} characters")

if __name__ == "__main__":
    mbz_file = "backup-moodle2-activity-2600518-book2600518-20260108-1341-nu.mbz"
    output_file = "oppimateriaali-2600518-20260108.md"
    
    if not os.path.exists(mbz_file):
        print(f"Error: {mbz_file} not found")
        sys.exit(1)
    
    extract_and_convert(mbz_file, output_file)

