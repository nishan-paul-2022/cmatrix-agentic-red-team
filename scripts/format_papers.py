import os
import re
import glob
import string

INPUT_DIR = "docs/paper-research/md-downloaded-paper-curated"

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

def extract_first_sentence(text):
    match = re.split(r'(?<=[.!?])\s+', text.strip())
    if match:
        return match[0]
    return text

def format_markdown(content):
    lines = content.split('\n')
    formatted_lines = []
    
    headings = []
    in_code_block = False
    
    for line in lines:
        if line.startswith('```'):
            in_code_block = not in_code_block
        if not in_code_block:
            m = re.match(r'^(#{1,4})\s+(.*)', line)
            if m:
                headings.append((len(m.group(1)), m.group(2).strip()))
                
    toc = ["## Table of Contents\n"]
    for level, title in headings:
        if level > 1:
            indent = "  " * (level - 2)
            # Remove markdown syntax from title for TOC
            clean_title = re.sub(r'[*_`]', '', title)
            toc.append(f"{indent}- [{clean_title}](#{slugify(clean_title)})")
    
    toc_str = "\n".join(toc) + "\n\n---\n"
    
    in_abstract = False
    in_code_block = False
    title_processed = False
    toc_inserted = False
    
    for i, line in enumerate(lines):
        if line.startswith('```'):
            in_code_block = not in_code_block
            formatted_lines.append(line)
            continue
            
        if in_code_block:
            formatted_lines.append(line)
            continue
            
        # First heading becomes title and gets TOC after it
        if not title_processed and (line.startswith('# ') or line.startswith('## ')):
            # If it's ## make it # for the title
            if line.startswith('## '):
                line = '# ' + line[3:]
            formatted_lines.append(line)
            title_processed = True
            continue
            
        if title_processed and not toc_inserted and not line.strip():
            formatted_lines.append('')
            formatted_lines.append(toc_str)
            toc_inserted = True
            continue
            
        if line.startswith('## '):
            if formatted_lines and formatted_lines[-1] != '---':
                if len(formatted_lines) > 10:
                    if formatted_lines[-1] != '':
                        formatted_lines.append('')
                    formatted_lines.append('---')
                    formatted_lines.append('')
            
            j = i + 1
            while j < len(lines):
                if lines[j].startswith('#') or lines[j].startswith('```'):
                    break
                if lines[j].strip() and not lines[j].startswith('>'):
                    first_sentence = extract_first_sentence(lines[j])
                    if len(first_sentence) > 30 and len(first_sentence) < 200:
                        formatted_lines.append(line)
                        formatted_lines.append('')
                        formatted_lines.append(f'> **Section Summary:** {first_sentence}')
                        formatted_lines.append('')
                        line = None
                    break
                j += 1
                
        if line is None:
            continue
            
        # Bold important terms case-insensitive, but keep original case
        line = re.sub(r'\b(Important|Note|Key Takeaway|Result|Conclusion|Summary|Abstract|Objective|Methodology):\s', r'**\1:** ', line, flags=re.IGNORECASE)
        line = re.sub(r'\b(et al\.|i\.e\.|e\.g\.|a priori|in vitro|in vivo|ad hoc)\b', r'*\1*', line)
        
        if line.startswith('#') and 'abstract' in line.lower():
            in_abstract = True
            formatted_lines.append(line)
            continue
            
        if in_abstract:
            if line.startswith('#'):
                in_abstract = False
            elif line.strip() and not line.startswith('>'):
                line = '> ' + line
                
        # Safe dense paragraph breaking: only split if there are multiple sentences separated by ;
        # The previous one was aggressive. Let's make it only for bullet points if it's really long > 400
        if len(line) > 400 and ';' in line and not line.startswith('>'):
            parts = line.split(';')
            if len(parts) > 3:
                formatted_lines.append(parts[0] + ':\n' + '\n'.join([f'- {part.strip()}' for part in parts[1:]]))
                continue
                
        formatted_lines.append(line)
        
    return '\n'.join(formatted_lines)

def main():
    files = glob.glob(os.path.join(INPUT_DIR, "*.md"))
    count = 0
    for filepath in files:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        new_content = format_markdown(content)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        count += 1
            
    print(f"Successfully formatted {count} markdown files.")

if __name__ == "__main__":
    main()
