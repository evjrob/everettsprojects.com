import os
import yaml
import toml
from datetime import datetime

def convert_frontmatter(directory):
    # Loop through all .md files in the directory
    for filename in os.listdir(directory):
        if not filename.endswith('.md'):
            continue
            
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()

        # Check if file starts with YAML frontmatter
        if not content.startswith('---\n'):
            continue

        # Split content into frontmatter and body
        _, frontmatter, body = content.split('---\n', 2)
        
        try:
            # Parse YAML frontmatter
            data = yaml.safe_load(frontmatter)
            
            # Skip if no valid YAML
            if not data:
                continue
                
            # Create new TOML structure
            new_data = {
                'title': data.get('title', ''),
                'description': data.get('description', ''),
                'date': data.get('date', ''),
                'authors': [data.get('author', '')] if data.get('author') else []
            }
            
            # Combine categories and tags
            tags = set()
            if 'categories' in data:
                tags.update(data['categories'])
            if 'tags' in data:
                tags.update(data['tags'])
                
            # Add taxonomies section if there are tags
            if tags:
                new_data['taxonomies'] = {'tags': sorted(list(tags))}
            
            # Add everything else to extra (except tagazine)
            extra = {}
            for key, value in data.items():
                if (key not in ['title', 'description', 'date', 'author', 'categories', 
                               'tags', 'tagazine-media', 'layout', 'guid']):
                    extra[key] = value
                    
            if extra:
                new_data['extra'] = extra
            
            # Convert to TOML
            new_frontmatter = toml.dumps(new_data)
            
            # Write the new file
            new_content = f'+++\n{new_frontmatter}+++\n{body}'
            
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(new_content)
                
            print(f"Converted {filename}")
            
        except yaml.YAMLError as e:
            print(f"Error parsing YAML in {filename}: {e}")
        except Exception as e:
            print(f"Error processing {filename}: {e}")

# Usage
directory = "."
convert_frontmatter(directory)