from sqlalchemy import create_engine
from sqlalchemy_utils.functions import create_database, database_exists
from .db_model.base import Base
from .session_manager import session_scope


class DatabaseTransactionManager:
    """
    Manages database transactions
    """
    def __init__(
            self,
            db_name=None,
            db_host='localhost',
    ):

        connection_string = f'postgresql+psycopg2://{db_host}/{db_name}'

        self.engine = create_engine(connection_string)

    def create_db(self):
        """
        Creates database if it does not exist
        """

        if not database_exists(self.engine.url):
            create_database(self.engine.url)

    def create_all_tables(self, drop_existing_tables=False):
        """
        Creates all table models.
        :param drop_existing_tables: if True, drops all tables associate with Base from the database.
        """
        # drops any existing table in the database
        if drop_existing_tables:
            Base.metadata.drop_all(bind=self.engine)

        # creates all tables models
        Base.metadata.create_all(bind=self.engine)

    def load_records(self, table, record):
        """
        Updates table with a record
        :param table: table class to be updated
        :param record: record to be added
        """
        with session_scope(self.engine) as session:

            filtered_record = self.filter_record(table, record)
            session.merge(table(**filtered_record))

    @staticmethod
    def filter_record(table, record):
        """
        Remove arguments not present in a table from record
        """

        filtered_record = dict()

        for column, value in record.items():
            if column in table.__table__.columns.keys():
                filtered_record[column] = value

        return filtered_record
