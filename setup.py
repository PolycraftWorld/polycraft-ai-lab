from setuptools import find_packages, setup

from polycraft_lab.installation.post_pip_install import PostDevelopCommand, PostInstallCommand

with open('README.md', 'r') as file:
    long_description = file.read()

setup(
    name='polycraft-lab',
    version='0.1.0',
    author='Polycraft World',
    author_email='willie.chalmers@polycraftworld.com',
    description='A tool to help train RL agents in novel environments.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://polycraftworld.com',
    project_urls={
        'Bug Tracker': 'https://github.com/PolycraftWorld/polycraft-ai-lab/issues/',
        'Documentation': 'https://polycraftworld.github.io/polycraft-ai-lab/',
        'Source Code': 'https://github.com/PolycraftWorld/polycraft-ai-lab/',
    },
    packages=find_packages(),
    cmdclass={
        'develop': PostDevelopCommand,
        'install': PostInstallCommand,
    },
    install_requires=['gym'],
    classifiers=[
        'Programming Language :: Python :: 3',
        # TODO: Set open source license
        'Operating System :: OS Independent',
        'Development Status :: 3 - Alpha'
    ],
    python_requires='>=3.6',
)
