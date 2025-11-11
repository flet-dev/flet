from dataclasses import dataclass

__all__ = ["Finder"]


@dataclass
class Finder:
    """
    Finder is used to search for controls by different criteria.
    """

    id: int
    """
    Internal finder ID - corresponds to a Finder instance on Dart side.
    """

    count: int
    """
    The number of controls found by this finder.
    """

    index: int = 0
    """
    The index of the control to interact with when multiple controls are found.
    """

    @property
    def first(self) -> "Finder":
        """
        Returns a Finder that finds the first control found by this finder.
        """
        if self.count == 0:
            raise ValueError("No controls found by this finder.")
        return Finder(id=self.id, count=1, index=0)

    @property
    def last(self) -> "Finder":
        """
        Returns a Finder that finds the last control found by this finder.
        """
        if self.count == 0:
            raise ValueError("No controls found by this finder.")
        return Finder(id=self.id, count=1, index=self.count - 1)

    def at(self, index: int) -> "Finder":
        """
        Returns a Finder that finds the control at the given index.

        Args:
            index: The index of the control to find.
        """
        if index < 0 or index >= self.count:
            raise IndexError("Index out of range.")
        return Finder(id=self.id, count=1, index=index)
