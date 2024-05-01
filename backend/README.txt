In order for half of the functions to run, the Mimic dataset (unzipped) needs to be in the 'backend' folder

Scripts:
-startup.py: imports all libraries used, has a couple general functions
-columninfo.py: gives/compares information about .csv's and their columns
-connector.py: establishes mariadb connection, creates database, has functions for populating each table, exporting each table to a .csv file, and printing n rows of each table 
-populator.py: contains the general functions for populating the db with any .csv as well as functions that automatically populate the db with Mimic entries (hence why Mimic is necessary)
-main.py: the driver of the program (mainly serves as the testing ground for functions at this point)