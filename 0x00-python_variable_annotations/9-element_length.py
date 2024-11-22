#!/usr/bin/env python3
"""
9. Let's duck type an iterable object
"""

from typing import Tuple, Sequence, Iterable, List


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    """
    Return a list of tuples where each tuple contains
    an element from the input list and its length
    """
    return [(i, len(i)) for i in lst]
