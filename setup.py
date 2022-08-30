from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'A package with useful functions relating to space.'

setup(
    name="Spacemath",
    version=VERSION,
    author="Periareion (Anton Sollman)",
    author_email="<periareion05@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['numpy'],
    keywords=['space', 'math'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)

