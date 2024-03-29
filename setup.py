from setuptools import find_namespace_packages, setup

## requirements.txt
with open("requirement.txt", "r") as file:
    required_packages = [ln.strip() for ln in file.readlines()]

setup(
    name="suavaai",
    version="0.0",
    packages= find_namespace_packages(),
    install_requires= required_packages
)

