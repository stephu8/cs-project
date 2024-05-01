############################################
#   This file has several functions that   #
#   gather file names and column titles.   #
#   It also provides the SET class for     #
#   the storage of this data.              #
############################################

# list contents of directory recursively to find .csv files
def scandir(DIR):
    FILES=[]
    log(f'scandir: looking in directory \'{DIR}\'')
    # list contents of directory recursively
    for FILE in [os.path.join(dp, f) for dp, dn, fn in os.walk(os.path.expanduser(DIR)) for f in fn]:
        # if file ends in '.csv' then add to FILES list
        if FILE[len(FILE)-4:] == '.csv':
            log(f'scandir: found {FILE}')
            FILES.append(FILE)
    return FILES

# get column titles by listing cols from a given list of files csv
# can be used colttl(scandir(DIR)) to ^ for each file in directory DIR
def colttl(FILES):
    COLS = []
    for FILE in FILES:
        COLS.append(pd.read_csv(FILE).columns)
        log(f'colttl: found columns {COLS} in file \'{FILE}\'')
    return COLS

# return matching col titles and dtypes
def colmatch(COLS, COLS2):
    MATCHINGCOLS = []
    ## COLUMN NAME MATCHING
    for NAME in COLS if len(COLS) > len(COLS2) else COLS2:
        for NAME2 in COLS if len(COLS) < len(COLS2) else COLS2:
            if NAME == NAME2:
                log(f'MATCH COLUMN {NAME}')
                MATCHINGCOLS.append(NAME)
    log(f'MATCH COLUMNS: {MATCHINGCOLS}')
    return MATCHINGCOLS

# if col1 and col2 have any matching
def colhasmatch(COLS, COLS2):
    ## COLUMN NAME MATCHING
    for NAME in COLS if len(COLS) > len(COLS2) else COLS2:
        for NAME2 in COLS if len(COLS) < len(COLS2) else COLS2:
            if NAME == NAME2:
                log(f'MATCH COLUMN {NAME}')
                return True
    return False

# make a new set from a given directory
class SET:
    def __init__(self, name):
        self.name=name              # directory name of set
        self.files=scandir(name)    # files in set
        self.cols=colttl(self.files)# column titles in each file SET.files[0] corisponds with SET.cols[0]
