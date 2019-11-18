"""A test example that loads a PALDynamicEnv and runs it."""

from pathlib import Path

from polycraft_lab.helpers import setup_env

CONFIG_FILE_PATH = str(Path(__file__).absolute().parent / 'pogo_stick_config.json')


def main(config_file_path: str = CONFIG_FILE_PATH):
    env = setup_env(config_file_path)
    for episode in range(0, 10):
        done = False
        step = 0
        while not done:
            action = env.action_space.sample()
            (observation, done, info) = env.step(action)
            step += 1
        print(f'Episode finished in {step + 1} steps')


if __name__ == '__main__':
    main()
