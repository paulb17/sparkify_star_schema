from sqlalchemy.ext.declarative import declarative_base, declared_attr
from .table_util import camel_to_snake_case


class Base():
    """
    Base class from which all mapped classes inherit
    """

    @declared_attr
    def __tablename__(cls):
        return camel_to_snake_case(cls.__name__)


Base = declarative_base(cls=Base)
