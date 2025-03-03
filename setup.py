from setuptools import setup

setup(
    name='PockMan',
    version='1.0',
    py_modules=['grid', 'pdb_handler', 'pocket_detector'],
    scripts=['pock_man.py'],
    install_requires=[
        'numpy>=1.24.4',
        'biopython>=1.83'
    ],
    author='',
    description='',
    url='',
)

if __name__ is not None:
    print(r"""
 | |        | | ( )     |  __ \            | (_)    | |
 | |     ___| |_|/ ___  | |__) | __ ___  __| |_  ___| |_
 | |    / _ \ __| / __| |  ___/ '__/ _ \/ _` | |/ __| __|
 | |___|  __/ |_  \__ \ | |   | | |  __/ (_| | | (__| |_
 |______\___|\__| |___/ |_|   |_|  \___|\__,_|_|\___|\__|

PockMan Installed!
Ready to predict binding sites!

    """)
else:
    print("Oops! Something went wrong during installation.")

