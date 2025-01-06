import csv
import os
from pathlib import Path

# Read the CSV file
print("Starting to process files...")
with open('Prompts_Database.csv', 'r', encoding='utf-8') as csv_file:
    reader = csv.DictReader(csv_file)
    count = 0
    for row in reader:
        try:
            # Get filename from URL
            filename = row['Prompt URL'].split('/')[-1]
            filepath = Path(filename)
            
            print(f"Processing {filename}")
            
            # Create frontmatter
            frontmatter = f"""---
title: "{row['Name']}"
tags: [{', '.join(f'"{tag.strip()}"' for tag in row['Prompt Tags'].split(','))}]
type: "{row['Type']}"
created: "{row['Created time']}"
url: "{row['Prompt URL']}"
---

"""
            
            # Read original content if file exists
            if filepath.exists():
                with open(filepath, 'r', encoding='utf-8') as md_file:
                    content = md_file.read()
                
                # Check if frontmatter already exists
                if not content.startswith('---'):
                    # Write new content with frontmatter
                    with open(filepath, 'w', encoding='utf-8') as md_file:
                        md_file.write(frontmatter + content)
                    count += 1
                    print(f"Updated {filename}")
                
        except Exception as e:
            print(f"Error processing {filename}: {str(e)}")
            
    print(f"Completed! Updated {count} files")
