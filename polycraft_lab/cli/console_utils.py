import os
from pathlib import Path


def _get_path(prompt: str) -> Path:
    """Get a path inputted from user input.

    Args:
        prompt (str): The question or prompt to display to the user

    Returns:
        A valid path inputted by the user.
    """
    while True:
        result = input(prompt)
        if os.path.isdir(result):
            path = Path(result)
            return path
        print('That is not a valid path.')


def _get_bool_input(prompt: str, default: bool = None) -> bool:
    """Get a response to a yes/no question.

    Args:
        prompt (str): The question or prompt to display to the user
        default (bool): If True, the user will be able to select a yes without
            having to input an explicit yes answer

    Returns:
        True if the prompt receives a yes answer, False otherwise.
    """
    while True:
        # TODO: Simplify this if tree
        if default is None:
            prompt_append = '[y/n]'
        elif default:
            prompt_append = '[Y/n]'
        else:
            prompt_append = '[y/N]'
        result = str(input(f'{prompt} {prompt_append} ')).lower()
        if default is None:
            if result == 'y':
                return True
            elif result == 'n':
                return False
            print('A response is required.')
            continue
        elif default:
            if result == 'y' or result == '':
                return True
            elif result == 'n':
                return False
        elif result == 'n':
            return False
        print('That is not a valid response.')
