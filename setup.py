from setuptools import setup, find_packages

setup(
    name='PockMan',
    version='1.0',
    packages=find_packages(),
    py_modules=['pdb_handler'],
    scripts=['pock_man.py'],
    install_requires=[
        'numpy>=1.24.4',
        'biopython>=1.83',
        'tqdm>=4.64.0',
    ],
    author='',
    description='',
    url='',
)

if __name__ is not None:
    print(r"""
PPPPPPPPPPPPPPPPP                                       kkkkkkkk
P::::::::::::::::P                                      k::::::k
P::::::PPPPPP:::::P                                     k::::::k
PP:::::P     P:::::P                                    k::::::k
  P::::P     P:::::P  ooooooooooo       cccccccccccccccc k:::::k    kkkkkkk   mmmmmmm    mmmmmmm     aaaaaaaaaaaaa  nnnn  nnnnnnnn
  P::::P     P:::::Poo:::::::::::oo   cc:::::::::::::::c k:::::k   k:::::k  mm:::::::m  m:::::::mm   a::::::::::::a n:::nn::::::::nn
  P::::PPPPPP:::::Po:::::::::::::::o c:::::::::::::::::c k:::::k  k:::::k  m::::::::::mm::::::::::m  aaaaaaaaa:::::an::::::::::::::nn
  P:::::::::::::PP o:::::ooooo:::::oc:::::::cccccc:::::c k:::::k k:::::k   m::::::::::::::::::::::m           a::::ann:::::::::::::::n
  P::::PPPPPPPPP   o::::o     o::::oc::::::c     ccccccc k::::::k:::::k    m:::::mmm::::::mmm:::::m    aaaaaaa:::::a  n:::::nnnn:::::n
  P::::P           o::::o     o::::oc:::::c              k:::::::::::k     m::::m   m::::m   m::::m  aa::::::::::::a  n::::n    n::::n
  P::::P           o::::o     o::::oc:::::c              k:::::::::::k     m::::m   m::::m   m::::m a::::aaaa::::::a  n::::n    n::::n
  P::::P           o::::o     o::::oc::::::c     ccccccc k::::::k:::::k    m::::m   m::::m   m::::ma::::a    a:::::a  n::::n    n::::n
PP::::::PP         o:::::ooooo:::::oc:::::::cccccc:::::ck::::::k k:::::k   m::::m   m::::m   m::::ma::::a    a:::::a  n::::n    n::::n
P::::::::P         o:::::::::::::::o c:::::::::::::::::ck::::::k  k:::::k  m::::m   m::::m   m::::ma:::::aaaa::::::a  n::::n    n::::n
P::::::::P          oo:::::::::::oo   cc:::::::::::::::ck::::::k   k:::::k m::::m   m::::m   m::::m a::::::::::aa:::a n::::n    n::::n
PPPPPPPPPP            ooooooooooo       cccccccccccccccckkkkkkkk    kkkkkkkmmmmmm   mmmmmm   mmmmmm  aaaaaaaaaa  aaaa nnnnnn    nnnnnn

PockMan Installed!
Ready to predict binding sites!

    """)
else:
    print("Oops! Something went wrong during installation.")

