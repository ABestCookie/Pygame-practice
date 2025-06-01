from cx_Freeze import setup, Executable

setup(
    name="DinoGame",
    version="0.1",
    description="Pygame game",
    executables=[Executable("main.py")]
)
