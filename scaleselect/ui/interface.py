"""
Author: Gregg Oliva
"""
# stdlib imports
from typing import List

# 3rd-party imports
from textual.app import ComposeResult
from textual.containers import (
    Container,
    Horizontal,
    Vertical,
    VerticalScroll,
)
from textual.reactive import reactive
from textual.widgets import (
    Button,
    Collapsible,
    Input,
    OptionList,
    Rule,
    SelectionList,
    Static,
)
from textual.widgets.option_list import Option

# project imports
from defs import (
    Accidental,
    Natural,
    ScaleType,
    ALL_ACCIDENTALS,
    ALL_KEYS,
    ALL_SCALE_TYPES,
)
from scales import ExcludeType


class Title(Static):
    pass


class ResultDisplay(Static):
    RESULTS_DISPLAY_ID = "results_display_option_list"
    GENERATE_NUMBER_ID = "number_to_generate_input"
    GENERATE_RESULTS_ID = "generate_results_button"
    OPTIONS_ROW_ID = "options_row"

    num_scales = 0

    def on_mount(self) -> None:
        # Default number of scales to generate
        scale_input = self.query_one(f"#{self.GENERATE_NUMBER_ID}", Input)
        self.num_scales = int(scale_input.value)

    def compose(self) -> ComposeResult:
        yield OptionList(
            Option("Run to display scales", disabled=True),
            id=self.RESULTS_DISPLAY_ID,
        )
        yield Horizontal(
            Button(
                "Generate",
                id=self.GENERATE_RESULTS_ID
            ),
            Input(
                "2",
                placeholder="# of Scales",
                type="integer",
                max_length=2,
                id=self.GENERATE_NUMBER_ID,
            ),
            id=self.OPTIONS_ROW_ID
        )

    def on_input_changed(self, event: Input.Changed) -> None:
        input_id = event.input.id

        if input_id == self.GENERATE_NUMBER_ID:
            try:
                value = int(event.input.value)
            except:
                value = 0
            self.num_scales = int(value)

    def on_button_pressed(self, event: Button.Pressed):
        button_id = event.button.id

        if button_id == self.GENERATE_RESULTS_ID:
            scales = self.app.scale_builder.get_random(self.num_scales)
            scales_display = self.query_one(f"#{self.RESULTS_DISPLAY_ID}", OptionList)

            scales_display.clear_options()
            scales_display.add_options(scales)


class SelectBase(Vertical):
    # Which exclude list to update
    EXCLUDE_TYPE: ExcludeType | None = None

    # ID of SelectionList
    SELECTION_LIST_ID: str | None = None

    # Selection Type
    SELECTION_TYPE_LIST: List[Natural | Accidental | ScaleType] = None

    # Collapsible Title
    COLLAPSIBLE_TITLE: str | None = None

    # Set of selected attributes
    selected = reactive(set())

    def on_mount(self) -> None:
        selected = []

        for select_type in self.SELECTION_TYPE_LIST:
            selected.append(
                (select_type.name.capitalize(), select_type, True)
            )

        selection_list = self.app.query_one(f"#{self.SELECTION_LIST_ID}", SelectionList)
        selection_list.clear_options()
        selection_list.add_options(selected)

    def watch_selected(self, selected: List[Natural | Accidental | ScaleType]) -> None:
        excluded_types = set()

        for select_type in self.SELECTION_TYPE_LIST:
            if select_type not in selected:
                excluded_types.add(select_type)

        self.app.scale_builder.update_excludes(self.EXCLUDE_TYPE, excluded_types)
        self.app.scale_builder.build_scales()

    def on_selection_list_selected_changed(self, event: SelectionList.SelectedChanged):
        selection_list_id = event.selection_list.id

        if selection_list_id == self.SELECTION_LIST_ID:
            self.selected = set(event.selection_list.selected)

    def compose(self) -> ComposeResult:
        yield Collapsible(
            SelectionList(
                *self.selected,
                id=self.SELECTION_LIST_ID,
            ),
            title=self.COLLAPSIBLE_TITLE,
        )


class KeySelect(SelectBase):
    EXCLUDE_TYPE = ExcludeType.KEYS
    SELECTION_LIST_ID = "key_selection_list"
    SELECTION_TYPE_LIST = ALL_KEYS
    COLLAPSIBLE_TITLE = "Select Keys"


class ScaleTypeSelect(SelectBase):
    EXCLUDE_TYPE = ExcludeType.SCALE_TYPES
    SELECTION_LIST_ID = "scale_type_selection_list"
    SELECTION_TYPE_LIST = ALL_SCALE_TYPES
    COLLAPSIBLE_TITLE = "Select Scale Types"


class AccidentalSelect(SelectBase):
    EXCLUDE_TYPE = ExcludeType.ACCIDENTALS
    SELECTION_LIST_ID = "accidentals_selection_list"
    SELECTION_TYPE_LIST = ALL_ACCIDENTALS
    COLLAPSIBLE_TITLE = "Select Accidentals"


class Content(Container):
    def compose(self) -> ComposeResult:
        yield VerticalScroll(
            ResultDisplay(),
            KeySelect(),
            ScaleTypeSelect(),
            AccidentalSelect(),
        )


class HomePage(Vertical):
    CONTENT_ID = "main_content"

    def compose(self) -> ComposeResult:
        yield Title("Welcome to ScaleZ")
        yield Rule()
        yield Content(id=self.CONTENT_ID)
