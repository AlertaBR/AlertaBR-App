from setuptools import setup, find_packages

# Lê o conteúdo do requirements.txt
with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="AlertaBR",
    version="1.0.0",
    description="App que exibe risco de enchente com base em localização e dados meteorológicos.",
    author="Equipe AlertaBR",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=requirements,
    python_requires=">=3.8"
)