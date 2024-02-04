"""
Author: Gregg Oliva
"""
def capitalize_all(s: str, delimiter: str = "_") -> str:
    return " ".join(
        [
            word.capitalize()
            for word in s.split(delimiter)
        ]
    )
