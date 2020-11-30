"""Configuration for installing this package using pip or setuptools."""
import pathlib
from pathlib import Path

from setuptools import find_namespace_packages, setup

from polycraft_lab.installation.post_pip_install import PostDevelopCommand, \
    PostInstallCommand

parent = pathlib.Path(__file__).parent

long_description = (parent / 'README.md').read_text()

# automatically captured required modules for install_requires in
# requirements.txt
with open(str(Path(parent) / 'requirements.txt'), encoding='utf-8') as f:
    package_dependencies = f.read().split('\n')

setup(
    name='polycraft_lab',
    version='0.1.0',
    author='Polycraft World',
    author_email='willie.chalmers@polycraftworld.com',
    description='A tool to help train RL agents in novel environments.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    entry_points={
        'console_scripts': [
            'pal=polycraft_lab:run_cli',
        ],
    },
    url='https://polycraftworld.com',
    project_urls={
        'Bug Tracker': 'https://github.com/PolycraftWorld/polycraft-ai-lab/issues/',
        'Documentation': 'https://polycraftworld.github.io/polycraft-ai-lab/',
        'Source Code': 'https://github.com/PolycraftWorld/polycraft-ai-lab/',
    },
    packages=find_namespace_packages(),
    cmdclass={
        'develop': PostDevelopCommand,
        'install': PostInstallCommand,
    },
    install_requires=package_dependencies,
    classifiers=[
        'Programming Language :: Python :: 3',
        # TODO: Set open source license
        'Operating System :: OS Independent',
        'Development Status :: 3 - Alpha'
    ],
    python_requires='>=3.6',
)
