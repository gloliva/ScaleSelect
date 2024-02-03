"""
Author: Gregg Oliva
"""
# stdlib imports
import sys

# project imports
from ui.app import ScaleZ


def main() -> int | None:
    app = ScaleZ()
    app.setup()
    app.run()
    return app.return_code


# Program entrypoint
if __name__ == "__main__":
    sys.exit(main() or 0)
