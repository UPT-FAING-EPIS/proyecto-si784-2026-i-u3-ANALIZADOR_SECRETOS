"""
build_exe.py – Build a standalone executable using PyInstaller.

Usage
-----
    python build_exe.py

Output
------
    dist/secret-scanner.exe   (Windows)
    dist/secret-scanner        (Linux / macOS)
"""

import PyInstaller.__main__

PyInstaller.__main__.run([
    "main.py",
    "--onefile",
    "--name",
    "secret-scanner",
    "--noconfirm",
])
