"""Unit tests for touch-struct functionality."""

import os
import shutil
import tempfile
import unittest
from pathlib import Path

from touch_struct import create_structure

class TestTouchStruct(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for each test
        self.test_dir = tempfile.mkdtemp()
        self.maxDiff = None

    def tearDown(self):
        # Clean up the temporary directory after each test
        shutil.rmtree(self.test_dir)

    def assert_path_exists(self, path):
        """Assert that a path exists relative to the test directory."""
        full_path = os.path.join(self.test_dir, path)
        self.assertTrue(os.path.exists(full_path), f"Path does not exist: {path}")

    def assert_is_dir(self, path):
        """Assert that a path is a directory relative to the test directory."""
        full_path = os.path.join(self.test_dir, path)
        self.assertTrue(os.path.isdir(full_path), f"Path is not a directory: {path}")

    def assert_is_file(self, path):
        """Assert that a path is a file relative to the test directory."""
        full_path = os.path.join(self.test_dir, path)
        self.assertTrue(os.path.isfile(full_path), f"Path is not a file: {path}")

    def test_basic_structure_from_string(self):
        """Test creating a basic structure from a string."""
        structure = """
project/
├── src/
│   └── main.py
└── README.md
"""
        create_structure.from_string(structure, self.test_dir)

        self.assert_is_dir("project")
        self.assert_is_dir("project/src")
        self.assert_is_file("project/src/main.py")
        self.assert_is_file("project/README.md")

    def test_nested_structure(self):
        """Test creating a deeply nested directory structure."""
        structure = """
deep-nest/
├── level1/
│   ├── level2/
│   │   ├── level3/
│   │   │   └── deep_file.txt
│   │   └── mid_file.py
│   └── side_file.js
└── root_file.md
"""
        create_structure.from_string(structure, self.test_dir)

        self.assert_is_dir("deep-nest")
        self.assert_is_dir("deep-nest/level1")
        self.assert_is_dir("deep-nest/level1/level2")
        self.assert_is_dir("deep-nest/level1/level2/level3")
        self.assert_is_file("deep-nest/level1/level2/level3/deep_file.txt")
        self.assert_is_file("deep-nest/level1/level2/mid_file.py")
        self.assert_is_file("deep-nest/level1/side_file.js")
        self.assert_is_file("deep-nest/root_file.md")

    def test_spaces_in_names(self):
        """Test creating structure with spaces in file and directory names."""
        structure = """
My Project/
├── Source Files/
│   ├── Main Program.py
│   └── Helper Functions.py
└── Documentation Files/
    └── Read Me First.txt
"""
        create_structure.from_string(structure, self.test_dir)

        self.assert_is_dir("My Project")
        self.assert_is_dir("My Project/Source Files")
        self.assert_is_dir("My Project/Documentation Files")
        self.assert_is_file("My Project/Source Files/Main Program.py")
        self.assert_is_file("My Project/Source Files/Helper Functions.py")
        self.assert_is_file("My Project/Documentation Files/Read Me First.txt")

    def test_from_file(self):
        """Test creating structure from a file."""
        # Create a temporary structure file
        structure = """
test-project/
├── docs/
│   └── index.md
└── code/
    └── app.py
"""
        structure_file = os.path.join(self.test_dir, "structure.txt")
        with open(structure_file, "w", encoding="utf-8") as f:
            f.write(structure)

        # Create the structure from the file
        create_structure.from_file(structure_file, self.test_dir)

        self.assert_is_dir("test-project")
        self.assert_is_dir("test-project/docs")
        self.assert_is_dir("test-project/code")
        self.assert_is_file("test-project/docs/index.md")
        self.assert_is_file("test-project/code/app.py")

    def test_complex_structure(self):
        """Test creating a complex structure with mixed file types and depths."""
        structure = """
web-app/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Header.tsx
│   │   │   └── Footer.tsx
│   │   ├── pages/
│   │   │   └── Home Page.tsx
│   │   └── index.ts
│   ├── public/
│   │   └── assets/
│   │       ├── images/
│   │       │   └── logo.png
│   │       └── styles/
│   │           └── main.css
│   └── package.json
└── backend/
    ├── src/
    │   ├── controllers/
    │   │   └── user controller.py
    │   └── models/
    │       └── user model.py
    └── requirements.txt
"""
        create_structure.from_string(structure, self.test_dir)

        # Test frontend structure
        self.assert_is_dir("web-app/frontend")
        self.assert_is_dir("web-app/frontend/src/components")
        self.assert_is_file("web-app/frontend/src/components/Header.tsx")
        self.assert_is_file("web-app/frontend/src/components/Footer.tsx")
        self.assert_is_dir("web-app/frontend/src/pages")
        self.assert_is_file("web-app/frontend/src/pages/Home Page.tsx")
        self.assert_is_file("web-app/frontend/src/index.ts")
        self.assert_is_dir("web-app/frontend/public/assets/images")
        self.assert_is_dir("web-app/frontend/public/assets/styles")
        self.assert_is_file("web-app/frontend/public/assets/images/logo.png")
        self.assert_is_file("web-app/frontend/public/assets/styles/main.css")
        self.assert_is_file("web-app/frontend/package.json")

        # Test backend structure
        self.assert_is_dir("web-app/backend")
        self.assert_is_dir("web-app/backend/src/controllers")
        self.assert_is_dir("web-app/backend/src/models")
        self.assert_is_file("web-app/backend/src/controllers/user controller.py")
        self.assert_is_file("web-app/backend/src/models/user model.py")
        self.assert_is_file("web-app/backend/requirements.txt")

    def test_multiple_roots(self):
        """Test creating multiple root directories."""
        structure = """
frontend/
├── src/
│   └── app.js
└── package.json
backend/
├── src/
│   └── server.py
└── requirements.txt
shared/
└── types.d.ts
"""
        create_structure.from_string(structure, self.test_dir)

        # Test frontend structure
        self.assert_is_dir("frontend")
        self.assert_is_dir("frontend/src")
        self.assert_is_file("frontend/src/app.js")
        self.assert_is_file("frontend/package.json")

        # Test backend structure
        self.assert_is_dir("backend")
        self.assert_is_dir("backend/src")
        self.assert_is_file("backend/src/server.py")
        self.assert_is_file("backend/requirements.txt")

        # Test shared structure
        self.assert_is_dir("shared")
        self.assert_is_file("shared/types.d.ts")

    def test_root_level_files(self):
        """Test creating files at the root level."""
        structure = """
README.md
LICENSE
src/
└── main.py
docs/
└── index.html
.gitignore
"""
        create_structure.from_string(structure, self.test_dir)

        # Test root level files
        self.assert_is_file("README.md")
        self.assert_is_file("LICENSE")
        self.assert_is_file(".gitignore")

        # Test directories and their contents
        self.assert_is_dir("src")
        self.assert_is_file("src/main.py")
        self.assert_is_dir("docs")
        self.assert_is_file("docs/index.html")

    def test_mixed_root_items(self):
        """Test creating a mix of files and directories at the root level."""
        structure = """
config.json
project1/
├── src/
│   └── app.py
└── tests/
    └── test_app.py
.env
project2/
└── main.js
README.md
"""
        create_structure.from_string(structure, self.test_dir)

        # Test root level files
        self.assert_is_file("config.json")
        self.assert_is_file(".env")
        self.assert_is_file("README.md")

        # Test project1 structure
        self.assert_is_dir("project1")
        self.assert_is_dir("project1/src")
        self.assert_is_dir("project1/tests")
        self.assert_is_file("project1/src/app.py")
        self.assert_is_file("project1/tests/test_app.py")

        # Test project2 structure
        self.assert_is_dir("project2")
        self.assert_is_file("project2/main.js")

if __name__ == '__main__':
    unittest.main() 