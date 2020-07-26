# Sparkify Analytics Database

## Introduction
This project involvee designing and creating an analytics database for a hypothetical start up called Sparkify. 
Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. 
To this end, a simple python based ETL pipeline was developed to extract data from local sources and load it into a star 
schema design. The choice to use a star schema was based on its high query performance relative to non-dimensional 
databases, its ease of use for end users and its ease of use with business intelligence tools.
## Requirements
Instructions for how to run assumes the following are installed:
* python 3.6+ and pip
* a package for managing virtual environments (e.g [venv](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)) 
* PostgreSQL ([One of many installation guides](https://www.datacamp.com/community/tutorials/installing-postgresql-windows-macosx))
        
Prior to running the code the following can be done on the command line:
* Navigate to folder where you want to store the repository
    ```commandline
    cd ~/path_to_folder/
    ``` 
  
* Clone the repository
    ```commandline
    git clone git@github.com:paulb17/sparkify_star_schema.git
    ```
  
* Change directoty to the sparkify_star_schema folder
    ```commandline
    cd sparkify_star_schema
    ``` 
  
* Create and activate a virtual environment
    ```commandline
     python3 -m venv venv
     source venv/bin/activate
    ```
* Install the needed packages 
    ```commandline
    pip install -r requirements.txt
    ```
* Ensure that a local PostgresSQL server is started
  
## Running the ETL pipeline
For an initial run, use the following command:
```commandline
   python3 etl.py 
```

By default the above command will create all tables in the database (dropping any existing table), extract the data,
from local files, transform the data, and load the data into the database tables. To simply drop any pre-existing table 
in the Sparkify database and recreate empty ones, run the following command can be run:

```commandline
   python3 create_tables.py
```

## Some improvements that could be made:
* Inclusion of surrogate keys in the design
* Addition of unit tests
* Better software architecture for the ETL process
* If speed is of concern, bulk loading of data into the database can be considered
