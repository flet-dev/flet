from dataclasses import dataclass


@dataclass
class Finder:
    """
    Finder is used to search for controls by different criterias.
    """

    id: int
    """
    Internal finder ID - corresponds to a Finder instance on Dart side.
    """

    count: int
    """
    The number of controls found by this finder.
    """
