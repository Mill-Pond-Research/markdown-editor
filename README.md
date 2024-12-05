# Markdown Editor

A simple web-based Markdown editor application built with Flask. This application allows you to create, read, update, and delete Markdown files with a live preview feature.

## Features

- Create and edit Markdown files
- Live preview of Markdown content
- File management (create, edit, delete)
- Auto-save drafts
- YAML frontmatter support
- Responsive design

## First Time Setup

1. Clone or download this repository to your local machine

2. Make sure you have Python 3.7+ installed. You can check your Python version by running:
```bash
python --version
```

3. Set up a virtual environment (recommended):
   - On Windows:
   ```bash
   # Navigate to project directory
   cd path/to/markdown-editor
   
   # Activate the virtual environment
   .venv\Scripts\activate
   ```
   
   - On macOS/Linux:
   ```bash
   # Navigate to project directory
   cd path/to/markdown-editor
   
   # Activate the virtual environment
   source .venv/bin/activate
   ```

4. Install the required dependencies:
```bash
pip install -r requirements.txt
```

5. Run the application:
```bash
python app.py
```

6. Open your browser and navigate to `http://localhost:5000`

## Usage

- Click "New Document" to create a new Markdown file
- Use the editor on the left side to write Markdown content
- See the live preview on the right side
- Enter a filename (optional) and click "Save" to save your document
- View all your documents on the home page
- Edit or delete documents using the buttons next to each file

## File Storage

All Markdown files are stored in the `documents` directory in the root of the project. Each file includes YAML frontmatter with metadata such as creation and update timestamps.

## Markdown Tips

You can use standard Markdown syntax in your documents:

```markdown
# Heading 1
## Heading 2

**Bold text**
*Italic text*

- Bullet points
- Another point

1. Numbered list
2. Second item

[Link text](https://example.com)

> Blockquote
```

## Troubleshooting

1. If you see "command not found" when activating the virtual environment:
   - Make sure you're in the project directory
   - Check that the `.venv` directory exists
   - Try creating a new virtual environment: `python -m venv .venv`

2. If you get import errors after installing requirements:
   - Make sure your virtual environment is activated (you should see `(.venv)` in your terminal)
   - Try reinstalling the requirements: `pip install -r requirements.txt`

3. If the application won't start:
   - Check that port 5000 is not in use
   - Ensure you have proper permissions in the project directory
   - Verify that all dependencies are installed correctly

## Development

To exit the virtual environment when you're done:
```bash
deactivate
```

To reactivate it later, use the activation command from step 3 of the setup instructions.