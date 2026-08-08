"""Load the plugin as a package, whether or not Manuskript is beside it.

The plugin is a package at the repository root, and its own modules import
each other relatively, as the plugin runtime requires. That means the tests
cannot simply import a module by path: the package has to exist first.

Registered under its own name rather than under ``manuskript.plugins``, so
the tests run in a clone of this repository alone -- which is how anybody
who takes only the plugin will run them.
"""

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = "anchors"

if PACKAGE not in sys.modules:
    spec = importlib.util.spec_from_file_location(
        PACKAGE,
        ROOT / "__init__.py",
        submodule_search_locations=[str(ROOT)],
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules[PACKAGE] = module
    spec.loader.exec_module(module)
