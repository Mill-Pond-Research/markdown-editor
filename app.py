from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import markdown2
import frontmatter
from datetime import datetime

app = Flask(__name__)
DOCS_DIR = "documents"

# Create documents directory if it doesn't exist
if not os.path.exists(DOCS_DIR):
    os.makedirs(DOCS_DIR)

STARTER_TEMPLATE = '''---
title: My New Document
created: {created_date}
updated: {updated_date}
---
# Welcome to Your New Document!

This is a starter template to help you get familiar with Markdown formatting. Feel free to edit or delete this content.

## Text Formatting

You can make text **bold** or *italic*. You can also combine them for ***bold and italic***.

## Lists

### Unordered List
- First item
- Second item
  - Nested item
  - Another nested item
- Third item

### Ordered List
1. First step
2. Second step
3. Third step

## Links and Images

You can create [links to websites](https://example.com)

Images work similarly:
![Alt text for image](https://via.placeholder.com/150)

## Code Blocks

Inline code: `print("Hello World")`

Code block:
```python
def greet(name):
    return "Hello, " + name + "!"
```

## Quotes

> This is a blockquote. You can use it to emphasize important information or quote someone.
> 
> It can span multiple lines.

## Tables

| Header 1 | Header 2 | Header 3 |
|----------|----------|----------|
| Cell 1   | Cell 2   | Cell 3   |
| Cell 4   | Cell 5   | Cell 6   |

## Task Lists

- [x] Completed task
- [ ] Pending task
- [ ] Another pending task

---

Feel free to delete this content and start writing your own document. Happy writing!'''

@app.route('/')
def index():
    files = []
    for filename in os.listdir(DOCS_DIR):
        if filename.endswith('.md'):
            filepath = os.path.join(DOCS_DIR, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                post = frontmatter.load(f)
                files.append({
                    'filename': filename,
                    'title': post.get('title', filename[:-3]),
                    'created': post.get('created', ''),
                    'updated': post.get('updated', '')
                })
    return render_template('index.html', files=files)

@app.route('/new')
def new_document():
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    template_content = STARTER_TEMPLATE.format(
        created_date=current_time,
        updated_date=current_time
    )
    return render_template('editor.html', content=template_content)

@app.route('/edit/<filename>')
def edit_document(filename):
    filepath = os.path.join(DOCS_DIR, filename)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        return render_template('editor.html', filename=filename, content=content)
    return redirect(url_for('index'))

@app.route('/save', methods=['POST'])
def save_document():
    data = request.get_json()
    filename = data.get('filename', '')
    content = data.get('content', '')
    
    if not filename:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'document_{timestamp}.md'
    
    if not filename.endswith('.md'):
        filename += '.md'
    
    filepath = os.path.join(DOCS_DIR, filename)
    
    # Parse existing frontmatter or create new
    try:
        post = frontmatter.loads(content)
    except:
        post = frontmatter.Post(content)
    
    # Update metadata
    post.metadata['updated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if 'created' not in post.metadata:
        post.metadata['created'] = post.metadata['updated']
    
    # Save the file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(frontmatter.dumps(post))
    
    return jsonify({'success': True, 'filename': filename})

@app.route('/delete/<filename>', methods=['POST'])
def delete_document(filename):
    filepath = os.path.join(DOCS_DIR, filename)
    if os.path.exists(filepath):
        os.remove(filepath)
        return jsonify({'success': True})
    return jsonify({'success': False, 'error': 'File not found'})

@app.route('/preview', methods=['POST'])
def preview():
    content = request.get_json().get('content', '')
    # Remove frontmatter if present
    try:
        post = frontmatter.loads(content)
        content = post.content
    except:
        pass
    html = markdown2.markdown(content)
    return jsonify({'html': html})

if __name__ == '__main__':
    app.run(debug=True) 