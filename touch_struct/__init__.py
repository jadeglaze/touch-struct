"""
touch-struct - Create directory structures from text representations
"""

from .core import create_structure

__version__ = "0.1.0"

# Expose the functions directly at the package level
from_string = create_structure.from_string
from_file = create_structure.from_file

__all__ = ["from_string", "from_file", "create_structure"] 