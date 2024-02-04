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
    ExcludeType,
    ALL_ACCIDENTALS,
    ALL_KEYS,
    ALL_SCALE_TYPES,
)


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
        yield OptionList(
            Option("Run to display scales", disabled=True),
            id=self.RESULTS_DISPLAY_ID,
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

            if not scales:
                scales = [Option("No scales to display", disabled=True)]

            scales_display.clear_options()
            scales_display.add_options(scales)


class SelectBase(Vertical):
    # Which exclude list to update
    EXCLUDE_TYPE: ExcludeType | None = None

    # ID of SelectionList
    NUM_SELECTION_LISTS: int | None = None
    SELECTION_LIST_ID_PREFIX: str | None = None

    # Selection Type
    SELECTION_TYPE_LIST: List[Natural | Accidental | ScaleType] = None

    # Collapsible Title
    COLLAPSIBLE_TITLE: str | None = None

    # Shared Classes
    SELECTION_LIST_CLASS: str | None = None
    COLLAPSIBLE_CONTAINER_CLASS = "collapsible_container"

    def on_selection_list_selected_changed(self, event: SelectionList.SelectedChanged):
        selection_list_id = event.selection_list.id
        index = int(selection_list_id.split("_")[-1])
        selected = event.selection_list.selected

        self.app.selection_manager.update_selections(
            selected,
            self.EXCLUDE_TYPE,
            index,
        )
        excluded_selections = self.app.selection_manager.get_excluded_selections(
            self.EXCLUDE_TYPE,
            index,
        )

        self.app.scale_builder.update_excludes(self.EXCLUDE_TYPE, excluded_selections)
        self.app.scale_builder.build_scales()

    def compose(self) -> ComposeResult:
        # Init the selection bank
        self.app.selection_manager.init_selection_bank(
            self.NUM_SELECTION_LISTS,
            self.SELECTION_TYPE_LIST,
            self.EXCLUDE_TYPE,
        )

        # Create the selection list objects
        selection_lists = [
            SelectionList(
                *self.app.selection_manager.get_selection_list_entries(self.EXCLUDE_TYPE, num),
                id=f"{self.SELECTION_LIST_ID_PREFIX}_{num}",
                classes=self.SELECTION_LIST_CLASS
            )
            for num in range(self.NUM_SELECTION_LISTS)
        ]

        yield Collapsible(
            Horizontal(
                *selection_lists,
                classes=self.COLLAPSIBLE_CONTAINER_CLASS,
            ),
            title=self.COLLAPSIBLE_TITLE,
        )


class KeySelect(SelectBase):
    EXCLUDE_TYPE = ExcludeType.KEYS
    NUM_SELECTION_LISTS = 3
    SELECTION_LIST_ID_PREFIX = "key_selection_list"
    SELECTION_TYPE_LIST = ALL_KEYS
    COLLAPSIBLE_TITLE = "Select Keys"
    SELECTION_LIST_CLASS = "key_selection_list"


class ScaleTypeSelect(SelectBase):
    EXCLUDE_TYPE = ExcludeType.SCALE_TYPES
    NUM_SELECTION_LISTS = 1
    SELECTION_LIST_ID_PREFIX = "scale_type_selection_list"
    SELECTION_TYPE_LIST = ALL_SCALE_TYPES
    COLLAPSIBLE_TITLE = "Select Scale Types"
    SELECTION_LIST_CLASS = "scale_type_selection_list"


class AccidentalSelect(SelectBase):
    EXCLUDE_TYPE = ExcludeType.ACCIDENTALS
    NUM_SELECTION_LISTS = 1
    SELECTION_LIST_ID_PREFIX = "accidentals_selection_list"
    SELECTION_TYPE_LIST = ALL_ACCIDENTALS
    COLLAPSIBLE_TITLE = "Select Accidentals"
    SELECTION_LIST_CLASS = "accidental_selection_list"


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
