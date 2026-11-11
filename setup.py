# Execute a partir desta pasta: python setup.py build
from cx_Freeze import Executable, setup

setup(
    name='ABYSS COCKPIT',
    version='1.0',
    description='DEPTH ZERO - jogo academico com Pygame',
    options={'build_exe': {
        'packages': ['pygame', 'pyttsx3', 'Recursos'],
        'include_files': [('bases', 'bases')],
    }},
    # Console necessario para input() ao pedir o nome do jogador.
    executables=[Executable('jogo.py', target_name='AbyssCockpit')],
)
