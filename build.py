import os
import sys
import py_compile
import re

PLUGIN_FILE = "Transcribe.plugin"

def build():
    print("Building Transcriber plugin...")
    if not os.path.exists(PLUGIN_FILE):
        print(f"Error: {PLUGIN_FILE} not found!")
        sys.exit(1)

    with open(PLUGIN_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Ensure author is @mm1vs
    content = re.sub(r'__author__\s*=\s*["\'][^"\']+["\']', '__author__ = "@mm1vs"', content)

    with open(PLUGIN_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print("Verifying compilation...")
    try:
        py_compile.compile(PLUGIN_FILE, doraise=True)
        print("Build successful! Transcribe.plugin is valid and ready.")
    except py_compile.PyCompileError as e:
        print(f"Compilation error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    build()
