from typing import Optional
import pathlib
import _pytest.pathlib

resolve_pkg_path_orig = _pytest.pathlib.resolve_package_path

# we consider all dirs in repo/ to be namespace packages
root_dir = pathlib.Path(__file__).parent.resolve()
namespace_pkg_dirs = [str(d) for d in root_dir.iterdir() if d.is_dir()]


# patched method
def resolve_package_path(path: pathlib.Path) -> Optional[pathlib.Path]:
    # call original lookup
    result = resolve_pkg_path_orig(path)
    if result is None:
        result = path  # let's search from the current directory upwards
    for parent in result.parents:
        if str(parent) in namespace_pkg_dirs:
            return parent
    return None

# apply patch
_pytest.pathlib.resolve_package_path = resolve_package_path
