import dataclasses


@dataclasses.dataclass
class Dimensions:
    width: int | float
    height: int | float


class DimensionsError(Exception):
    pass
