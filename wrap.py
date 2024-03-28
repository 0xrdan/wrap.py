"""
WrapPy
v0.1
Just a simple Python executor
by Dan Monteiro aka 0xrDan
"""

import tkinter as tk
from tkinter import filedialog
import subprocess
import re

# Define color scheme for Python syntax highlighting
python_colors = {
    "keyword": "cyan",
    "built_in": "orange",
    "function": "red",
    "string": "green",
    "number": "purple",
    "comment": "grey",
    "method": "yellow"
}

def load_file():
    """ Open a file dialog to select a Python file and load it into the text editor. """
    filename = filedialog.askopenfilename()
    with open(filename, 'r', encoding='utf-8') as file:
        code_text.delete('1.0', tk.END)
        code_text.insert(tk.END, file.read())
        highlight_syntax()

def highlight_syntax():
    """ Highlight syntax elements in the code editor based on predefined patterns. """
    code = code_text.get("1.0", tk.END)
    code_text.tag_remove("keyword", "1.0", tk.END)
    code_text.tag_remove("built_in", "1.0", tk.END)
    code_text.tag_remove("string", "1.0", tk.END)
    code_text.tag_remove("number", "1.0", tk.END)
    code_text.tag_remove("comment", "1.0", tk.END)
    code_text.tag_remove("method", "1.0", tk.END)
    code_text.tag_remove("function", "1.0", tk.END)

    # Regular expressions for syntax highlighting
    patterns = [
        (r'\b(?:open|True|False|None)\b', "built_in"),
        (r'\b(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)\b', "number"),
        (r'\'\'\'(.*?)\'\'\'|\"\"\"(.*?)\"\"\"', "string"),  # Multiline string
        (r'\'(?:\\.|[^\'\\])*\'|\"(?:\\.|[^\"\\])*\"', "string"),  # Single-line string
        (
            r'\b(?:import|from|as|def|class|for|if|else|elif|while|return'
            r'|try|except|finally|with|pass|break|continue|in)\b',
            "keyword"
        ),
        (
            r'# .*?(?=\n|$\b(?!#\b[0-9a-fA-F]{6}\b)|\n|$)',
            "comment"
        ),  # Matches comments excluding hex color codes
        (
            r'(?<!\w\.)\b\w+\s*(?=\()',
            "function"
        ),  # Matches function names followed by "(" with no text immediately preceding it
        (
            r'\.\s*(\w+)(?=\()',
            "method"
        ),  # Matches words preceding "(" and after "."
        (
            r'\b#[0-9a-fA-F]{6}\b',
            "string"
        )  # Hex color code
    ]

    for pattern, tag in patterns:
        for match in re.finditer(pattern, code):
            start = match.start()
            end = match.end()
            code_text.tag_add(tag, f"1.0+{start}c", f"1.0+{end}c")
            code_text.tag_configure(tag, foreground=python_colors[tag])

def execute_code():
    """ Execute Python code in text editor and display the output in the output text area. """
    code = code_text.get('1.0', tk.END)
    output_text.delete('1.0', tk.END)
    try:
        # Redirect stdout to a variable
        result = subprocess.run(
            ["python", "-c", code],
            capture_output=True,
            text=True,
            check=False
        )
        output_text.insert(tk.END, result.stdout)
        if result.stderr:
            output_text.insert(tk.END, f"Error: {result.stderr}")
    except Exception as e:
        output_text.insert(tk.END, f"Error: {str(e)}")

# Create the main Tkinter window
root = tk.Tk()
root.title("WrapPy: Just a simple Python executor - by 0xrDan")

# Create and configure the "Load File" button
load_button = tk.Button(root, text="Load File", command=load_file)
load_button.pack()

# Create the text area for Python code input
code_text = tk.Text(root, height=20, width=80, bg="#1e1e1e", fg="#ffffff")
code_text.pack()
code_text.bind("<KeyRelease>", highlight_syntax)

# Create and configure the "Execute Code" button
execute_button = tk.Button(root, text="Execute Code", command=execute_code)
execute_button.pack()

# Create and configure the output text label
output_label = tk.Label(root, text="Output:")
output_label.pack()

# Create the text area for displaying output
output_text = tk.Text(root, height=10, width=80, bg="#1e1e1e", fg="#ffffff")
output_text.pack()

root.mainloop()
