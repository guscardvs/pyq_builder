import dataclasses

from pyq_builder.utils.comparison import Comparator


@dataclasses.dataclass
class Parameter:
    field: str
    escaped_field: str
    comparator: Comparator
    position: int

    def parametrize(self):
        return f":{self.field}"

    def __str__(self):
        return self.comparator.stringify(
            field=self.escaped_field,
            parameter=self.parametrize(),
        )
