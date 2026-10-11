import py_compile
import re
import sys
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PLUGIN_FILE = ROOT / "Transcribe.plugin"
ELYX_FILE = ROOT / "Transcribe.elyx"


def metadata_value(source, key, default=""):
    match = re.search(rf"^{re.escape(key)}\s*=\s*['\"]([^'\"]*)['\"]", source, re.MULTILINE)
    return match.group(1) if match else default


def build():
    print("Building Transcriber plugin and Elyx package...")
    if not PLUGIN_FILE.exists():
        print(f"Error: {PLUGIN_FILE.name} not found!")
        sys.exit(1)

    content = PLUGIN_FILE.read_text(encoding="utf-8")
    # Keep the published author consistent in both package formats.
    content = re.sub(
        r'(?m)^__author__\s*=\s*["\'][^"\']+["\']',
        '__author__ = "@mm1vs"',
        content,
    )
    PLUGIN_FILE.write_text(content, encoding="utf-8")

    plugin_id = metadata_value(content, "__id__", "Transcribe")
    plugin_name = metadata_value(content, "__name__", "Transcriber")
    version = metadata_value(content, "__version__")
    min_version = metadata_value(content, "__min_version__", "11.12.0")
    icon = metadata_value(content, "__icon__", "monek_icons/1")
    if not version:
        raise ValueError("Could not read __version__ from Transcribe.plugin")

    refmap = "metainfo: plugin/meta.yml\nmain: plugin/main.py\nelyxbuilder: plugin/.elyxbuilder\n"
    meta = (
        f"name: {plugin_name}\n"
        'description: "Replaces Telegram\'s transcription service with free AI alternatives."\n'
        f"id: {plugin_id}\n"
        f'version: "{version}"\n'
        'author: "@mm1vs"\n'
        f'app_version: ">={min_version}"\n'
        f"icon: {icon}\n"
    )
    elyx_config = "zipFormat: eaf\nsource: plugin\n"

    print("Verifying Python syntax...")
    try:
        py_compile.compile(str(PLUGIN_FILE), doraise=True)
    except py_compile.PyCompileError as exc:
        print(f"Compilation error: {exc}")
        sys.exit(1)

    with zipfile.ZipFile(ELYX_FILE, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("refmap.yml", refmap)
        archive.writestr("plugin/meta.yml", meta)
        archive.writestr("plugin/main.py", content)
        archive.writestr("plugin/.elyxbuilder/config.yml", elyx_config)

    print(f"Build successful: {PLUGIN_FILE.name} v{version} and {ELYX_FILE.name}")


if __name__ == "__main__":
    build()
