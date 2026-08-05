import re
import glob

files = glob.glob("docs/paper-research/md-downloaded-paper-curated/*.md")

count = 0
for file_path in files:
    with open(file_path, 'r') as f:
        lines = f.readlines()
        
    new_lines = []
    modified = False
    for line in lines:
        if re.match(r'^\d+\s*$', line):
            modified = True
            continue
        new_lines.append(line)
        
    if modified:
        count += 1
        with open(file_path, 'w') as f:
            f.write("".join(new_lines))
            
print(f"Removed stray page numbers from {count} files.")
