from cx_Freeze import setup, Executable

# Lê as dependências do requirements.txt
with open("requirements.txt") as f:
    packages = [line.strip() for line in f if line.strip() and not line.startswith("#")]

target = [ Executable(
    script="main.py",            
    target_name="AlertaBR.exe",  
    base="WIN32GUI",
    icon="assets/icon.ico"
) ]

build_exe_options = {
    "packages": packages,
    "include_files": ["assets/icon.ico"],
    "include_msvcr": True
}

setup(
    name="AlertaBR",
    version="1.0",
    description="Aplicativo de previsão climática em tempo real e alerta de enchentes em até 7 dias",
    author="Equipe AlertaBR",
    url="https://github.com/AlertaBR/AlertaBR-App/blob/main/README.md",
    license="MIT",
    keywords=["weather", "flood", "tkinter", "customtkinter", "openstreetmap", "open-meteo", "python"],
    options={"build_exe": build_exe_options},
    executables=target
)
