import re
import tomllib
import pathlib
import typer
import rich
from enum import Enum

app = typer.Typer()

class PinType(str, Enum):
    eq = "=="
    ge = ">="


def get_package_version(package:str) -> list[str|None]:
    package_version = re.split(r'==|>=|<=|>|<', package, maxsplit=1)

    if len(package_version) == 1:
        package_version.append(None)

    return package_version


def get_requirements() -> dict[str, str | None]:
    requirements_in = pathlib.Path('requirements.in').read_text()

    packages = {}

    for package in requirements_in.splitlines():
        package, version = get_package_version(package)
        packages[package] = version

    return packages

@app.command()
def check_versions() -> dict[str, str | None]:
    """Checks the version of the python packages in the manifest"""

    packages = get_requirements()

    with open('./pyproject.toml', 'rb') as pyproject_path:
        pyproject = tomllib.load(pyproject_path)

    for package_path in pyproject['tools']['version_check']['paths']:
        package, package_path = package_path.split(':')

        with open(pathlib.Path(package_path).joinpath('pyproject.toml'), 'rb') as toml_path:
            toml_path = tomllib.load(toml_path)

        if (version:= toml_path['project']['version']) != packages[package]:
            rich.print(f"{package=} {version=} does not match current version {packages[package]}")
            packages[package] = version
        
        else:
            del packages[package]

    return packages

@app.command()
def update(pin: PinType = PinType.eq):
    """Updates the requirements"""

    requirements = get_requirements()
    requirements.update(check_versions())
    updated_requirements = [pin.value.join([package, version]) for package, version in requirements.items()]
    pathlib.Path('requirements.in').write_text('\n'.join(updated_requirements))


if __name__ == "__main__":
    app()


