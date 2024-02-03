"""
Author: Gregg Oliva
"""
# stdlib imports
import os
from typing import List


# Filepath
PATH = os.path.dirname(os.path.abspath(__file__))
STYLES_DIRECTORY = os.path.join(PATH, "../..", "styles")


def get_css_files() -> List[str]:
    filenames = os.listdir(STYLES_DIRECTORY)
    style_files = [
        os.path.join(STYLES_DIRECTORY, filename)
        for filename in filenames
        if filename.endswith(".tcss")
    ]

    return style_files
