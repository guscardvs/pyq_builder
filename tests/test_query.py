from dataclasses import dataclass

import pytest

from pyq_builder import exc
from pyq_builder.pyq_builder import QBuilder
from pyq_builder.query.expression import select
from pyq_builder.query.filters import Field
from pyq_builder.query.main import Query


@dataclass
class MyObject:
    name: str
    value: int


class NoDataclassObject:
    pass


def test_query_should_return_valid_fieldnames_when_receiving_dataclass(
    q_builder: QBuilder,
):
    assert q_builder.acquire_query(Query, klass=MyObject).fieldnames == (
        "name",
        "value",
    )


def test_query_should_return_valid_fields_with_types_when_receiving_dataclass(
    q_builder: QBuilder,
):
    assert q_builder.acquire_query(Query, klass=MyObject).fields == {
        "name": str,
        "value": int,
    }


def test_query_should_raise_invalid_class_when_class_is_not_dataclass(
    q_builder: QBuilder,
):
    with pytest.raises(exc.UnsupportedClass) as exc_info:
        q_builder.acquire_query(Query, klass=NoDataclassObject)
    assert exc_info.value.args == (
        "this class is not supported, use dataclass instead",
    )


def test_query_should_use_lower_classname_for_tablename_when_not_receiving_table_param(
    q_builder: QBuilder,
):
    assert (
        q_builder.acquire_query(Query, klass=MyObject).table
        == MyObject.__name__.lower()
    )


def test_query_should_use_table_param_when_receiving_it(
    q_builder: QBuilder,
):
    assert (
        q_builder.acquire_query(
            Query,
            klass=MyObject,
            table="table",
        ).table
        == "table"
    )


def test_list_should_return_valid_querystring_when_receiving_class(
    q_builder: QBuilder,
):
    assert (
        str(select(MyObject).get(q_builder.dialect).where(Field("name")))
        == "SELECT `name`, `value` FROM `myobject` WHERE `name` = :name"
    )
