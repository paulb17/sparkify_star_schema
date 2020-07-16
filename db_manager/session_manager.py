"""
Creating a session scope to keep the lifecycle of the session separate and external from functions
and objects that access and/or manipulate database data. This will greatly help with achieving a
predictable and consistent transactional scope.
"""

from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker


@contextmanager
def session_scope(engine):
    """
    Provide a transactional scope around a series of operations.
    :param engine: the sqlalchemy engine for the database
    """
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

