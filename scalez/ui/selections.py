"""
Author: Gregg Oliva
"""
# stdlib imports
from typing import List, Set, Tuple

# project imports
from defs import (
    Accidental,
    Natural,
    ScaleType,
    ExcludeType,
    ALL_EXCLUDED_TYPES,
)
from helpers import capitalize_all


class SelectionManager:
    def __init__(self) -> None:
        self.selected = {
            exclusion_type.value: {}
            for exclusion_type in ALL_EXCLUDED_TYPES
        }
        self.num_selected = {
            exclusion_type.value: {}
            for exclusion_type in ALL_EXCLUDED_TYPES
        }

    def init_selection_bank(
            self,
            num_selection_lists: int,
            selection_list: List[Natural | Accidental | ScaleType],
            selection_type: ExcludeType,
        ) -> None:
        for index in range(num_selection_lists):
            self.selected[selection_type.value][index] = {}
            self.num_selected[selection_type.value][index] = 0

        num_types = len(selection_list)
        threshold = num_types // num_selection_lists

        for num, select_type in enumerate(selection_list):
            index = num // threshold
            self.selected[selection_type.value][index][select_type] = True
            self.num_selected[selection_type.value][index] += 1

    def get_selection_list_entries(self, selection_type: ExcludeType, index: int) -> List[Tuple]:
        selections = self.selected[selection_type.value][index]
        selection_list_entries = [
            (capitalize_all(selection.name), selection, enabled)
            for selection, enabled in selections.items()
        ]
        return selection_list_entries

    def update_selections(self, selection_list_entries: List, selection_type: ExcludeType, index: int) -> None:
        selections = self.selected[selection_type.value][index]
        selection_list_entries = set(selection_list_entries)

        for selection in selections.copy().keys():
            enabled = False if selection not in selection_list_entries else True
            selections[selection] = enabled

    def get_excluded_selections(self, selection_type: ExcludeType) -> Set:
        all_selections = self.selected[selection_type.value]
        excluded_selections = set()

        for selection_section in all_selections.values():
            for selection, enabled in selection_section.items():
                if not enabled:
                    excluded_selections.add(selection)

        return excluded_selections
