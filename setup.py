from cx_Freeze import setup, Executable
import sys
import os

base = None
if sys.platform == "win32":
    base = "Win32GUI"  # sem console

# Caminhos
main_script = "main.py"
icon_path = os.path.join("asset", "icon", "icon.ico")

# Opções de build
build_exe_options = {
    "packages": ["pygame", "os", "sys", "random"],
    "include_files": [("code", "code")],  # inclui pasta com os .py
    "excludes": ["tkinter"],
}

# Setup final
setup(
    name="MoraMigos",
    version="1.0",
    description="Jogo dos Gatinhos",
    options={"build_exe": build_exe_options},
    executables=[
        Executable(
            script=main_script,
            base=base,
            target_name="MoraMigos.exe",
            icon=icon_path  # ← ícone incluído
        )
    ]
)
