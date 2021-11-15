import pytest

from pyq_builder.dialects.base import Driver
from pyq_builder.pyq_builder import QBuilder


@pytest.fixture(scope="function")
def q_builder():
    return QBuilder(driver=Driver.POSTGRES)
