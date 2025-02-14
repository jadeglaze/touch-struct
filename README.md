# touch-struct

A tool to create directory and file structures from text representations like the ones you might get from ChatGPT.

## Installation

You can install via pip:

```bash
pip install touch-struct
```

## Usage

`touch-struct` can be used both as a command-line tool and as a Python library.

### Command Line Usage

The most convenient (but maybe not obvious) way to use `touch-struct` may be to paste the structure directly into your terminal like this:

1. Copy the structure you want to create into your clipboard. (Usually from ChatGPT or similar)
2. In your terminal, go to the directory you want to create the structure in.
3. Type `touch-struct -` (the dash is important!) and hit enter.
4. Paste the structure into the terminal.
5. Press Ctrl+D (which means "end of file") to finish.
6. Voila! The structure is created!

There are however a few other ways to use it:

```bash
# Create from a file
touch-struct structure.txt

# Create in a specific directory
touch-struct structure.txt --output-dir my-new-project

# Create from stdin (pipe)
cat structure.txt | touch-struct -
```

### Python Library Usage

```python
import touch_struct

# Create from a string
structure = """
project/
├── src/
│   ├── main.py
│   └── utils.py
├── tests/
│   └── test_main.py
├── README.md
└── setup.py
"""
touch_struct.from_string(structure)

# Create from a file
touch_struct.from_file("structure.txt")

# Create in a specific directory
touch_struct.from_string(structure, base_path="my-new-project")
touch_struct.from_file("structure.txt", base_path="my-new-project")
```

## Structure Format

The tool accepts a text representation of directory structures using ASCII characters:
- Use `/` at the end of a line to indicate directories
- Use standard ASCII characters (`├`, `│`, `└`, `─`) to draw the tree structure
- Indentation and structure characters are used to determine hierarchy

Example structure file:
```
my-project/
├── src/
│   ├── main.py
│   └── utils.py
├── tests/
│   └── test_main.py
└── docs/
    ├── index.md
    └── api.md
```

You can also create multiple root directories or files:
```
README.md
LICENSE
frontend/
├── src/
│   └── app.js
└── package.json
backend/
├── src/
│   └── server.py
└── requirements.txt
```

### Tips
- Files shouldn't have a trailing slash: `README.md`
- Directories need a trailing slash: `src/`
- Spaces in names are supported: `My Project/`
- You can mix files and directories at any level
- The structure can be as deep as you need
- Root level can contain multiple files and directories

## Contributing

For detailed information about contributing, including how to make releases, please see [CONTRIBUTING.md](CONTRIBUTING.md).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details. 