from setuptools import find_packages, setup

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
    url='https://github.com/PolycraftWorld/polycraft-ai-lab',
    packages=find_packages(),
    install_requires=['gym'],
    classifiers=[
        'Programming Language :: Python :: 3',
        # TODO: Set open source license
        'Operating System :: OS Independent'
    ],
    python_requires='>=3.6',
)
