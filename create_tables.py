from etl import SparkifyETL

"""
Script to create database and create Sparkify star schema tables. 
Existing tables will be dropped prior to creating new tables.
"""

if __name__ == '__main__':

    etl_obj = SparkifyETL(drop_existing_tables=True)
    etl_obj.create_sparkify_tables()
