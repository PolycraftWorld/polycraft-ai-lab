# Polycraft AI Lab (PAL)
*A tool to help train reinforcement learning models to handle novel environments.*

## About
Polycraft AI Lab consists of a wrapper for Polycraft World game environments.
These environments can used to train RL models that respond to novel tasks
and scenarios.

## Usage

### 1a. Install via package
First, download Polycraft AI Lab using pip:
```shell script
pip install polycraft-lab
```

This downloads the `polycraft-lab` package from pip, which contains tools to
easily set up and manage the Polycraft game client.

To install the most recent changes (experimental version):
```shell script
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://test.pypi.org/simple/ polycraft-lab
```

### 1b. Local Installation
Alternatively, to install the latest version from source:
```shell script
git clone https://github.com/PolycraftWorld/polycraft-ai-lab
pip install ./polycraft-ai-lab
```

If you installed PAL using method (1a), this isn't required.

### 2. Import and Use
Now train your agent like you would do with any other gym-style environment:
```python
from polycraft_lab.envs.helpers import setup_env

env = setup_env('pogo_stick')
observation = env.reset()
for _ in range(1000):
    env.render()
    action = env.action_space.sample() # your agent here (this takes random actions)
    observation, reward, done, info = env.step(action)

    if done:
        observation = env.reset()
env.close()
```

Polycraft AI Lab also contains a wrapper [WIP] to start experiment creation from
the command line. The following begins the experiment creation process by
launching Minecraft:
```shell script
python -m polycraft_lab.ect --create EXPERIMENT_NAME --launch
``` 

Running `python -m polycraft_lab.ect --create EXPERIMENT_NAME` will allow you to
create simpler experiments, allowing configuration of more high-level domain
attributes, like action space and a preconfigured goal, such as finding
diamonds as quickly as possible.

## Development
Clone out the repository:
```shell script
git clone https://github.com/PolycraftWorld/polycraft-ai-lab.git
```

Optionally, you can create a virtual environment to store dependencies.

In any case, install the dependencies:
```shell script
pip install -r requirements.txt
```

Alternatively, a virtual environment can be created with the necessary
dependencies by running:
```shell script
cd polycraft-ai-lab
pipenv install
```

### Distribution
Polycraft AI Lab will be distributed using pip.

The easy way to upload to upload to the test PyPI index:
```shell script
./release.sh
```

To release to the live PyPI index:
```shell script
./release.sh --release
```
