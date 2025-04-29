import shutil
from pathlib import Path

use_sphinx = {{cookiecutter.sphinx_documentation}}
documentation_dir = Path.cwd() / "docs"

# Cookiecutter doesn't yet appear to support conditionals in directory names.
# Instead, the directory is always created and this script will delete it if
# the user didn't want it.
if not use_sphinx:
    shutil.rmtree(documentation_dir)
