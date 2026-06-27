from __future__ import annotations


class CodeGrader:
    """A simple binary grader for code solutions."""

    def score(self, output: object, expected: object | None = None) -> float:
        if expected is None:
            return 1.0 if bool(output) else 0.0
        return 1.0 if output == expected else 0.0
