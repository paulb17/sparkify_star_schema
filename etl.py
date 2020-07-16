import os
import glob
import json

from datetime import datetime
from sql_queries import SparkifyDBQueries
from db_manager.db_model.sparkify_schema import *
from db_manager.db_model.table_util import camel_to_snake_case


class SparkifyETL:
    """
    Class consists of a run_etl method which creates database and tables if they do not exist,
    extracts log and song JSON data, transforms the data and loads it into facts and dimension
    tables.
    """
    def __init__(
            self,
            drop_existing_tables=False
    ):

        # initializing database transaction manager
        self.dbtm = SparkifyDBQueries(
            db_name='sparkifydb',
            db_host='localhost'
        )

        self.drop_existing_tables = drop_existing_tables

        # placeholder copy of processed log data
        self.processed_log_records = None

    def run_etl(self):

        self.create_sparkify_tables()
        self.etl_for_log_data()
        self.etl_for_song_data()
        self.etl_for_sparkify_fact_tables()

    def create_sparkify_tables(self):
        """
        Function to create database and tables for the sparkify star schema
        """

        # creating database and tables
        self.dbtm.create_db()
        self.dbtm.create_all_tables(drop_existing_tables=self.drop_existing_tables)

    def etl_for_log_data(self):
        """
        Extracts log data, transforms it and loads it into the users and time dimension tables
        """
        # extract log data
        records = self.extract_data('data/log_data')

        for record in records:
            # transform log data
            record = self.process_log_data(record)

            # load log data
            self.load_data(record, log_data_dimensions)

        # create a copy of processed records for updating fact table
        self.processed_log_records = list(records)

    def etl_for_song_data(self):
        """
        Extracts log data, transforms it and loads it into the song and artist dimension tables
        """

        # extract song data
        records = self.extract_data('data/song_data')

        # load song data
        for record in records:
            self.load_data(record, song_data_dimensions)

    def etl_for_sparkify_fact_tables(self):
        """
        Utilizes processed log data and dimension table queries to load the fact tables
        """

        for record in self.processed_log_records:

            record = self.process_fact_table_record(record)

            self.load_data(record, sparkify_facts)

    def extract_data(self, filepath):
        """
        Extracts data from all JSON files at a specified path and stores it as a list of records
        """
        records = []

        json_files = self.get_json_file_paths(filepath)

        for json_file in json_files:
            records += self.read_json_file(json_file)

        return records

    @staticmethod
    def read_json_file(json_file):
        """
        Extracts data from a JSON file and stores it as a list of records
        """
        file_records = list()

        for line in open(json_file, 'r'):
            file_records.append(json.loads(line))

        return file_records

    @staticmethod
    def get_json_file_paths(filepath):
        """
        Retrives all JSON files at the specified file path and in a subdirectory of the specified path
        :param filepath: the relative file path to search
        :return all_files: list of absolute paths for all JSON files
        """
        all_files = []
        for root, dirs, files in os.walk(filepath):
            files = glob.glob(os.path.join(root, '*.json'))
            for f in files:
                all_files.append(os.path.abspath(f))

        return all_files

    def process_log_data(self, record):
        """
        :param record: unprocessed record
        :return: processed record
        """
        # filter out certain records
        if record['page'] != 'NextSong':
            return

        record = self.adding_time_fields(record)
        record = self.renaming_camel_case_fields(record)

        return record

    @staticmethod
    def adding_time_fields(record):
        """
        Adds time fields to log data record
        """

        start_time = datetime.fromtimestamp(record['ts']/1000)

        record['start_time'] = start_time
        record['hour'] = start_time.hour
        record['day'] = start_time.day
        record['week'] = start_time.strftime('%W')
        record['month'] = start_time.month
        record['year'] = start_time.year
        record['weekday'] = start_time.weekday()

        return record

    @staticmethod
    def renaming_camel_case_fields(record):
        """
        Converts some column names in log data records from camel case to snake case
        :param record: record with some column names in camel case
        :return: record with column names in snake case
        """
        for camel_case in ['userId', 'firstName', 'lastName', 'userAgent']:
            snake_case = camel_to_snake_case(camel_case)
            record[snake_case] = record[camel_case]
            record.pop(camel_case)

        return record

    def process_fact_table_record(self, record):
        """
        :param record: unprocessed record
        :return: processed record
        """

        # query to find song ID and artist ID
        artist_id, song_id = self.dbtm.song_fact_query(record)

        if song_id is None:
            return

        # add song ID and artist ID to record
        record['song_id'] = song_id
        record['artist_id'] = artist_id

        return record

    def load_data(self, record, tables):
        """
        Loads list of records into list of tables
        :param record: list of dictionary containing records to be loaded into the table
        :param tables: table classes for records to be loaded into
        """

        if record is not None:
            for table in tables:
                self.dbtm.load_records(table, record)


if __name__ == '__main__':

    etl = SparkifyETL(drop_existing_tables=True)
    etl.run_etl()
