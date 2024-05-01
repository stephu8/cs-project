import pandas as pd
import numpy as np
import mariadb
import sys
import os
import pickle
import re

############################################
#   This file hosts all the imports,       #
#   global variables, and some misc        #
#   functions.                             #
############################################
####################
# GLOBAL VARIABLES #
####################
LOGLVL = 1
STATEFILE = './savestate.pkl'
MIMICFILELOC='../Mimic'
CDCDEATHSFILELOC='../Deaths in the US CDC'
SETS = []

# print messages based on log level
def log(MSG):
    if LOGLVL == 1:
        print(MSG)

#compare two strings
def compare_strings(str1, str2):
    pattern = re.compile(str2)
    match = re.search(pattern, str1)
    return match
