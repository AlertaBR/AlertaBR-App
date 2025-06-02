from setuptools import setup, find_packages

setup(
    name="AlertaBR",
    version="0.1.0",
    description="Aplicação de alerta com mapa usando CustomTkinter",
    author="Luís Scacchetti",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    include_package_data=True,
    python_requires=">=3.8",
)
with open("requirements.txt") as f:
    requirements = f.read().splitlines()
