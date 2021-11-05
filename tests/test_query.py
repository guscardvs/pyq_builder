from dataclasses import dataclass

import pytest
from pyq_builder.query import Query
from pyq_builder import exc


@dataclass
class MyObject:
    name: str
    value: int


class NoDataclassObject:
    pass


def test_query_should_return_valid_fieldnames_when_receiving_dataclass():
    query = Query(MyObject)
    assert query.fieldnames == frozenset({"name", "value"})


def test_query_should_return_valid_fields_with_types_when_receiving_dataclass():
    query = Query(MyObject)
    assert query.fields == {"name": str, "value": int}


def test_query_should_raise_invalid_class_when_class_is_not_dataclass():
    with pytest.raises(exc.UnsupportedClass) as exc_info:
        Query(MyObject)
    assert exc_info.value.args == (
        "Class type is not supported, use dataclass instead",
    )
