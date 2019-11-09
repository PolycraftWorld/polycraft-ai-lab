# Polycraft AI Lab (PAL)
*A tool to help train reinforcement learning models to handle novel environments.*

## About
Polycraft AI Lab consists of a wrapper for OpenAI Gym along with a dynamic means
of loading environments for experiments created in the Polycraft AI Lab
Experiment Creation Tool (PAL-ECT).

These environments can used to train RL models that respond to novel environments.

Note: Experiments are not created using this tool; they are created using the
Experiment Creation Tool (which will eventually be in its own repository).

## Usage
**Note: this is an example of planned usage coming soon.**
```python
from tests import setup_env

POGO_EXPERIMENT_CONFIG_PATH = '/home/me/pogostick_challenge.json'

env = setup_env(POGO_EXPERIMENT_CONFIG_PATH)
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
```
python -m polycraft_lab.ect --create EXPERIMENT_NAME --launch
``` 

Running `python -m polycraft_lab.ect --create EXPERIMENT_NAME` will allow you to
create simpler experiments, allowing configuration of more high-level domain
attributes, like action space and a preconfigured goal, such as finding
diamonds as quickly as possible.

## Development
Clone out the repository:
```
git clone https://github.com/PolycraftWorld/polycraft-ai-lab.git
```

Create a virtual environment. Switch to the project's directory and then install
the project's dependencies using pipenv:
```
cd polycraft-ai-lab
pipenv install
```

Alternatively, install using pip:
```
pip install -r requirements.txt
```