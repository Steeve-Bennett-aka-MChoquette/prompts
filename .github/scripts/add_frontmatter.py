import csv
import os
from pathlib import Path

def main():
    print("Starting to process files...")
    
    # Get the root directory (where the script is run from)
    root_dir = Path.cwd()
    csv_path = root_dir / 'Prompts_Database.csv'
    
    if not csv_path.exists():
        print(f"Error: Cannot find {csv_path}")
        return
        
    try:
        with open(csv_path, 'r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            count = 0
            for row in reader:
                try:
                    # Get filename from URL
                    filename = row['Prompt URL'].split('/')[-1]
                    filepath = root_dir / filename
                    
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
                        with open(filepath, 'r', encoding='utf-8-sig') as md_file:
                            content = md_file.read()
                        
                        # Skip if frontmatter already exists
                        if not content.startswith('---'):
                            # Write new content with frontmatter
                            with open(filepath, 'w', encoding='utf-8') as md_file:
                                md_file.write(frontmatter + content)
                            count += 1
                            print(f"Updated {filename}")
                    else:
                        print(f"Warning: File not found - {filename}")
                
                except Exception as e:
                    print(f"Error processing {filename}: {str(e)}")
                    continue
                    
        print(f"Completed! Updated {count} files")
        
    except Exception as e:
        print(f"Error reading CSV: {str(e)}")

if __name__ == "__main__":
    main()
