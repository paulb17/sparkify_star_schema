from etl import SparkifyETL

"""
Script to create database and create Sparkify star shema tables. 
drop any existing tables. Any existing tables will be dropped
"""

if __name__ == '__main__':

    etl_obj = SparkifyETL(drop_existing_tables=True)
    etl_obj.create_sparkify_tables()
