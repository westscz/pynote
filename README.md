# PyNote (🐍🧾)

Turn Python file with Markdown formating in Docstrings into Markdown file.

This script will change one-to-one your python file into markdown file.
Your module level single and multi lines docstrings(`"""`) would be treat as
markdown code, the rest would be treat as python code.

## Background

**I'm not a fan of Jupyter Notebooks**.
In training courses, I wanted to teach students by showing them examples in
the IDE instead of presentations. Therefore, as part of the materials,
I always showed python code with comments written in docstrings.

Such materials have their great advantage, which is the ease of running them
on the student's environment and editing them without additional tools.

The downside is the limitation of the form. Jupyter Notebook allows you to
generate pdf/html files and in this case we are limited to python files.

The script was created to get rid of this limitation, supporting the creation
of markdown and html files based on the python file. It will also help me
create blog posts using executable python files.

## Getting Started

- Run script via `python pynote.py` (you can use `example/flask.py` for test)
- Open `output` directory to view the result.

## Example

So let's say that our python file looks likes this:

```python
"""
### Matching sequences

Your main loop will need to get input from the user and split it into words,
let’s say a list of strings like this:
"""
command = input("What are you doing next? ")
# analyze the result of command.split()
```

It will be converted to markdown code visible below:

---

### Matching sequences

Your main loop will need to get input from the user and split it into words,
let’s say a list of strings like this:

```py
command = input("What are you doing next? ")
# analyze the result of command.split()
```

---

More examples can be found in `example/` directory.

## Features

### HTML

You can also create HTML file with `--html` flag.

PyNote is using [Marked.js](https://marked.js.org/) as markdown code to html
converter, and [Highlight.js](https://highlightjs.org/) for syntax highlighting.

## Questions

Feel free to create an issue on Github.
