import re
import tomllib
import pathlib
import typer
import rich

app = typer.Typer()

def get_package_version(package:str) -> list[str|None]:
    package_version = re.split(r'==|>=|<=|>|<', package, maxsplit=1)

    if len(package_version) == 1:
        package_version.append(None)

    return package_version


@app.command()
def check_versions():
    """Checks the version of the python packages in the manifest"""

    with open('./pyproject.toml', 'rb') as f:
        pyproject = tomllib.load(f)
        packages = dict()

        for p in pyproject['project']['dependencies']:
            package, version = get_package_version(p)
            packages[package] = version

    for package_path in pyproject['tools']['version_check']['paths']:
        package, path = package_path.split(':')

        with open(pathlib.Path(path).joinpath('pyproject.toml'), 'rb') as toml_path:
            package_pyproject = tomllib.load(toml_path)
            if (version:= package_pyproject['project']['version']) != packages[package]:
                rich.print(f"{package=} {version=} does not match current version {packages[package]}")

@app.command()
def install_local():
    """Installs the local versions of packages"""

    with open('./pyproject.toml', 'rb') as f:
        pyproject = tomllib.load(f)
        packages = dict()

        for p in pyproject['project']['dependencies']:
            package, version = get_package_version(p)
            packages[package] = version

    for package_path in pyproject['tools']['version_check']['paths']:
        package, path = package_path.split(':')

        with open(pathlib.Path(path).joinpath('pyproject.toml'), 'rb') as toml_path:
            package_pyproject = tomllib.load(toml_path)
            if (version:= package_pyproject['project']['version']) != packages[package]:
                rich.print(f"{package=} {version=} does not match current version {packages[package]}")

if __name__ == "__main__":
    app()


