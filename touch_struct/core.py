"""Core functionality for parsing and creating directory structures."""

import os
import re
from typing import List, Optional

class StructureNode:
    def __init__(self, name: str, is_dir: bool = False):
        self.name = name
        self.is_dir = is_dir
        self.children: List[StructureNode] = []
        self.parent: Optional[StructureNode] = None

    def add_child(self, child: 'StructureNode') -> None:
        child.parent = self
        self.children.append(child)

    def get_full_path(self) -> str:
        """Get the full path of this node by traversing up to the root."""
        parts = []
        current = self
        while current.parent and current.parent.name:  # Stop at virtual root
            parts.append(current.name)
            current = current.parent
        if current.name:  # Add root name if not virtual root
            parts.append(current.name)
        return os.path.join(*reversed(parts)) if parts else ""

    def __str__(self):
        return f"{'[DIR]' if self.is_dir else '[FILE]'} {self.name}"

class StructureParser:
    TREE_CHARS = {
        '├': 'branch',
        '│': 'vertical',
        '└': 'last',
        '─': 'horizontal'
    }

    @staticmethod
    def clean_name(line: str) -> str:
        """Remove tree characters and leading/trailing whitespace from a line."""
        # First remove the tree characters
        name = re.sub(r'^[├└]─+\s*', '', line.strip())
        # Then remove any remaining tree characters that might be in the middle
        name = re.sub(r'[│├└─]\s*', '', name)
        return name

    @staticmethod
    def get_indent_level(line: str) -> int:
        """Calculate the indentation level of a line."""
        # Count leading spaces and tree characters
        indent = 0
        for i, char in enumerate(line):
            if char == ' ':
                indent += 1
            elif char in '│├└':
                # Tree characters contribute to indentation
                indent = (i // 4 + 1) * 4
            elif char == '─':
                continue
            else:
                break
        return indent // 4

    @staticmethod
    def is_root_level(line: str) -> bool:
        """Check if a line represents a root-level item."""
        # A line is root level if it has no leading spaces or tree characters
        return not bool(re.match(r'^\s*[│├└]', line))

    @staticmethod
    def parse(content: str) -> StructureNode:
        # Split into lines and remove empty lines
        lines = [line.rstrip() for line in content.split('\n') if line.strip()]
        
        # Find the minimum indentation level (ignoring empty lines)
        min_indent = min(len(line) - len(line.lstrip()) for line in lines)
        
        # Remove the common indentation from all lines
        lines = [line[min_indent:] for line in lines]
        
        root = StructureNode("", True)  # Virtual root node
        current_path = [root]
        prev_indent = 0

        print("\nParsing structure:")
        for line in lines:
            print(f"\nProcessing line: '{line}'")
            
            # Skip lines that are just tree characters
            clean_line = line.strip()
            if all(c in '│ ' for c in clean_line):
                print("Skipping tree-only line")
                continue

            # Calculate indentation level
            indent = StructureParser.get_indent_level(line)
            print(f"Indent level: {indent}")

            # Get clean name without tree characters
            name = StructureParser.clean_name(line)
            is_dir = name.endswith('/')
            if is_dir:
                name = name[:-1]
            print(f"Extracted name: '{name}', is_dir: {is_dir}")

            # Adjust the current path based on indentation
            if StructureParser.is_root_level(line):  # Root level item
                current_path = [root]
                print("Reset to root")
            elif indent > prev_indent:  # Going deeper
                print("Going deeper")
            elif indent < prev_indent:  # Going back up
                # Pop levels until we're at the right depth
                levels_to_pop = prev_indent - indent
                for _ in range(levels_to_pop):
                    if len(current_path) > 1:  # Keep at least the root
                        popped = current_path.pop()
                        print(f"Popped from path: {popped}")
            
            print(f"Current path: {' -> '.join(str(n) for n in current_path)}")

            # Create and add the new node
            node = StructureNode(name, is_dir)
            current_path[-1].add_child(node)
            print(f"Added node: {node}")
            
            if is_dir:
                current_path.append(node)
                print(f"Appended to path: {node}")
            
            prev_indent = indent

        return root

class StructureCreator:
    @staticmethod
    def create(node: StructureNode, base_path: str = ".") -> None:
        """Create the physical directory structure from a StructureNode."""
        if not node.name:  # Virtual root node
            print("\nCreating structure:")
            # For virtual root, directly process children
            for child in node.children:
                StructureCreator.create(child, base_path)
            return

        # Get the full path for this node
        node_path = node.get_full_path()
        current_path = os.path.join(base_path, node_path)
        print(f"Creating: {current_path} ({'directory' if node.is_dir else 'file'})")

        if node.is_dir:
            os.makedirs(current_path, exist_ok=True)
        else:
            # Create parent directories if they don't exist
            os.makedirs(os.path.dirname(current_path), exist_ok=True)
            # Create an empty file
            open(current_path, 'a').close()

        # Process children
        for child in node.children:
            StructureCreator.create(child, base_path)

class create_structure:
    @staticmethod
    def from_string(content: str, base_path: str = ".") -> None:
        """Create directory structure from a string representation."""
        parser = StructureParser()
        creator = StructureCreator()
        
        root = parser.parse(content)
        creator.create(root, base_path)

    @staticmethod
    def from_file(file_path: str, base_path: str = ".") -> None:
        """Create directory structure from a file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        create_structure.from_string(content, base_path) 