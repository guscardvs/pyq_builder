try:
    pass
except ImportError:
    print("You need to install pydantic in order to use PydanticMapper")
    raise

from .base import AbstractBaseMapper


class PydanticMapper(AbstractBaseMapper):
    pass
