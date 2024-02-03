"""
Author: Gregg Oliva
"""
# 3rd-party imports
from textual.app import App, ComposeResult
from textual.binding import Binding

# project imports
from scales import ScaleBuilder
from ui.interface import HomePage
from ui.styles import get_css_files


class ScaleZ(App[int]):
    CSS_PATH = get_css_files()
    BINDINGS = [
        Binding("q", "quit_app", "Quit App")
    ]

    def setup(self) -> None:
        self.scale_builder = ScaleBuilder()

    def compose(self) -> ComposeResult:
        yield HomePage()

    def action_quit_app(self) -> None:
        self.exit(0, return_code=0)
