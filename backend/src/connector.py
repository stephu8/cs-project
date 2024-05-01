############################################
#   Establishes connection with Clinical   #
#   Database.                              #
#   Requires mariadb                       #
############################################

import mariadb
import sys

try:
    con = mariadb.connect(
        user="root",    #Ryan: my mariadb is fighting me, changing user to 'root' for now for testing
        password="password",
        host="127.0.0.1",
        port=3306
    )

except mariadb.Error as e:
    print(f"Error connecting to MariaDB platform: {e}")
    sys.exit(1)

cursor = con.cursor()

#creating the database
query = "CREATE DATABASE IF NOT EXISTS clinicaldb"
cursor.execute(query)

#TABLES WITHOUT FOREIGN KEYS
#creating HOSPITAL table
query = "CREATE TABLE IF NOT EXISTS clinicaldb.HOSPITAL (hospital_id VARCHAR(45) NOT NULL, PRIMARY KEY (hospital_id), UNIQUE INDEX hospital_id_UNIQUE (hospital_id ASC) VISIBLE) ENGINE = InnoDB"
cursor.execute(query)

#creating HCPCS table
query = "CREATE TABLE IF NOT EXISTS clinicaldb.HCPCS (hcpcs_code VARCHAR(45) NOT NULL,category VARCHAR(45) NULL,long_desc VARCHAR(250) NULL,short_desc VARCHAR(75) NULL, PRIMARY KEY (hcpcs_code), UNIQUE INDEX hcpcs_code_UNIQUE (hcpcs_code ASC) VISIBLE) ENGINE = InnoDB"
cursor.execute(query)

#creating ICD table
query = "CREATE TABLE IF NOT EXISTS clinicaldb.ICD (icd_code VARCHAR(45) NOT NULL,icd_version INT NOT NULL,title VARCHAR(300) NULL, PRIMARY KEY (icd_code, icd_version)) ENGINE = InnoDB"
cursor.execute(query)

#creating LAB ITEM table
query = "CREATE TABLE IF NOT EXISTS clinicaldb.LAB_ITEM (item_id INT NOT NULL,name VARCHAR(45) NULL,fluid VARCHAR(45) NULL, category VARCHAR(45) NULL, PRIMARY KEY (item_id), UNIQUE INDEX item_id_UNIQUE (item_id ASC) VISIBLE) ENGINE = InnoDB"
cursor.execute(query)

#creating SUBJECT table
query = "CREATE TABLE IF NOT EXISTS clinicaldb.SUBJECT (subject_id INT NOT NULL,gender VARCHAR(1) BINARY NULL,age INT NULL, year_group VARCHAR(11) NULL,date_of_death DATE NULL,marital_status VARCHAR(45) NULL,race VARCHAR(45) NULL,language VARCHAR(45) NULL, PRIMARY KEY (subject_id), UNIQUE INDEX subject_id_UNIQUE (subject_id ASC) VISIBLE) ENGINE = InnoDB"
cursor.execute(query)

#TABLES WITH FOREIGN KEYS
#creating ADMISSION table
query = "CREATE TABLE IF NOT EXISTS clinicaldb.ADMISSION (subject_id INT NOT NULL,hospital_id VARCHAR(45) NULL,admittime DATETIME NOT NULL,dischtime DATETIME NULL,deathtime DATETIME NULL,admission_type VARCHAR(45) NULL,amit_provider_id VARCHAR(15) NULL, admission_location VARCHAR(45) NULL,discharge_location VARCHAR(45) NULL,insurance_type VARCHAR(45) NULL,edregtime DATETIME NULL,       edouttime DATETIME NULL,hospital_expire_flag INT NULL,PRIMARY KEY (subject_id, admittime),INDEX fk_ADMISSION_HOSPITAL1_idx (hospital_id ASC) VISIBLE,CONSTRAINT fk_ADMISSION_SUBJECT FOREIGN KEY (subject_id) REFERENCES clinicaldb.SUBJECT (subject_id) ON DELETE NO ACTION ON UPDATE NO ACTION, CONSTRAINT fk_ADMISSION_HOSPITAL1 FOREIGN KEY (hospital_id) REFERENCES clinicaldb.HOSPITAL (hospital_id) ON DELETE NO ACTION ON UPDATE NO ACTION) ENGINE = InnoDB"
cursor.execute(query)

#creating DIAGNOSIS table
query = "CREATE TABLE IF NOT EXISTS clinicaldb.DIAGNOSIS (subject_id INT NOT NULL,hospital_id VARCHAR(45) NULL,seq_num INT NULL,icd_code VARCHAR(45) NOT NULL,icd_version INT NULL,PRIMARY KEY (subject_id, icd_code),INDEX fk_DIAGNOSIS_HOSPITAL1_idx(hospital_id ASC) VISIBLE,INDEX fk_DIAGNOSIS_ICD1_idx (icd_code ASC, icd_version ASC) VISIBLE, CONSTRAINT fk_DIAGNOSIS_SUBJECT1 FOREIGN KEY (subject_id) REFERENCES clinicaldb.SUBJECT (subject_id) ON DELETE NO ACTION ON UPDATE NO ACTION,CONSTRAINT fk_DIAGNOSIS_HOSPITAL1    FOREIGN KEY (hospital_id) REFERENCES clinicaldb.HOSPITAL (hospital_id) ON DELETE NO ACTION ON UPDATE NO ACTION,CONSTRAINT fk_DIAGNOSIS_ICD1 FOREIGN KEY (icd_code , icd_version) REFERENCES clinicaldb.ICD (icd_code , icd_version) ON DELETE NO ACTION ON UPDATE NO ACTION) ENGINE = InnoDB"
cursor.execute(query)

#creating DRG table
query = "CREATE TABLE IF NOT EXISTS clinicaldb.DRG (subject_id INT NOT NULL,hospital_id VARCHAR(45) NOT NULL,drg_type VARCHAR(45) NOT NULL,drg_code INT NOT NULL,drg_severity INT NULL,drg_mortality INT NULL,description VARCHAR(100) NULL, PRIMARY KEY (subject_id, hospital_id, drg_code, drg_type), INDEX fk_DRG_HOSPITAL1_idx (hospital_id ASC) VISIBLE, CONSTRAINT fk_DRG_SUBJECT1 FOREIGN KEY (subject_id) REFERENCES clinicaldb.SUBJECT (subject_id) ON DELETE NO ACTION ON UPDATE NO ACTION, CONSTRAINT fk_DRG_HOSPITAL1 FOREIGN KEY (hospital_id) REFERENCES clinicaldb.HOSPITAL (hospital_id) ON DELETE NO ACTION ON UPDATE NO ACTION) ENGINE = InnoDB"
cursor.execute(query)

#creating HCPCS EVENT table
query = "CREATE TABLE IF NOT EXISTS clinicaldb.HCPCS_EVENT (subject_id INT NOT NULL, hospital_id VARCHAR(45) NULL, chartdate DATE NOT NULL, hcpcs_code VARCHAR(45) NOT NULL, seq_num INT NULL, short_description VARCHAR(100) NULL, PRIMARY KEY (subject_id, chartdate, hcpcs_code), INDEX fk_HCPCS_EVENT_HCPCS1_idx (hcpcs_code ASC) VISIBLE, INDEX fk_HCPCS_EVENT_HOSPITAL1_idx (hospital_id ASC) VISIBLE, CONSTRAINT fk_HCPCS_EVENT_HCPCS1 FOREIGN KEY (hcpcs_code) REFERENCES clinicaldb.HCPCS (hcpcs_code) ON DELETE NO ACTION ON UPDATE NO ACTION, CONSTRAINT fk_HCPCS_EVENT_SUBJECT1 FOREIGN KEY (subject_id) REFERENCES clinicaldb.SUBJECT (subject_id) ON DELETE NO ACTION ON UPDATE NO ACTION, CONSTRAINT fk_HCPCS_EVENT_HOSPITAL1 FOREIGN KEY (hospital_id) REFERENCES clinicaldb.HOSPITAL (hospital_id) ON DELETE NO ACTION ON UPDATE NO ACTION) ENGINE = InnoDB"
cursor.execute(query)

#creating MICROBIOLOGY EVENT table
query = "CREATE TABLE IF NOT EXISTS clinicaldb.MICROBIOLOGY_EVENT (microevent_id INT NOT NULL,subject_id INT NULL,hospital_id VARCHAR(45) NULL,microspecimen_id INT NULL,order_provider_id VARCHAR(45) NULL,chartdate DATETIME NULL,spec_item_id VARCHAR(45) NULL,  spec_type_desc VARCHAR(45) NULL,test_seq INT NULL,storedate DATETIME NULL,test_item_id INT NULL,test_name VARCHAR(45) NULL, org_item_id VARCHAR(45) NULL,org_name VARCHAR(45) NULL,isolate_num VARCHAR(45) NULL,quantity VARCHAR(45) NULL,ab_item_id VARCHAR(45) NULL,ab_name VARCHAR(45) NULL,dilution_text VARCHAR(45) NULL,dilution_comparison VARCHAR(45) NULL,dilution_value VARCHAR(45) NULL,interpretation VARCHAR(300) NULL, comments VARCHAR(1000) NULL, PRIMARY KEY (microevent_id), INDEX fk_MICROBIOLOGY_EVENT_HOSPITAL1_idx (hospital_id ASC) VISIBLE, INDEX fk_MICROBIOLOGY_EVENT_SUBJECT1_idx (subject_id ASC) VISIBLE, CONSTRAINT fk_MICROBIOLOGY_EVENT_SUBJECT1 FOREIGN KEY (subject_id) REFERENCES clinicaldb.SUBJECT (subject_id) ON DELETE NO ACTION ON UPDATE NO ACTION, CONSTRAINT fk_MICROBIOLOGY_EVENT_HOSPITAL1   FOREIGN KEY (hospital_id) REFERENCES clinicaldb.HOSPITAL (hospital_id) ON DELETE NO ACTION ON UPDATE NO ACTION) ENGINE = InnoDB"
cursor.execute(query)

#creating OMR table
query = "CREATE TABLE IF NOT EXISTS clinicaldb.OMR (subject_id INT NOT NULL,chartdate DATE NOT NULL,seq_num INT NULL, result_name VARCHAR(45) NOT NULL,result_value VARCHAR(45) NULL, PRIMARY KEY (subject_id, chartdate, result_name), CONSTRAINT fk_OMR_SUBJECT1 FOREIGN KEY (subject_id) REFERENCES clinicaldb.SUBJECT (subject_id) ON DELETE NO ACTION ON UPDATE NO ACTION) ENGINE = InnoDB"
cursor.execute(query)

#creating PROCEDURE_TABLE table (PROCEDURE in an SQL keyword and causes syntax errors)
query = "CREATE TABLE IF NOT EXISTS clinicaldb.PROCEDURE_TABLE (subject_id INT NOT NULL, hospital_id VARCHAR(45) NOT NULL, seq_num INT NOT NULL, chartdate DATE NOT NULL, icd_code VARCHAR(45) NOT NULL, icd_version INT NULL, PRIMARY KEY (subject_id, hospital_id, seq_num, icd_code, chartdate), INDEX fk_PROCEDURE_HOSPITAL1_idx (hospital_id ASC) VISIBLE, INDEX fk_PROCEDURE_ICD1_idx (icd_code ASC, icd_version ASC) VISIBLE, CONSTRAINT fk_PROCEDURE_SUBJECT1 FOREIGN KEY (subject_id) REFERENCES clinicaldb.SUBJECT (subject_id) ON DELETE NO ACTION ON UPDATE NO ACTION, CONSTRAINT fk_PROCEDURE_HOSPITAL1 FOREIGN KEY (hospital_id) REFERENCES clinicaldb.HOSPITAL (hospital_id) ON DELETE NO ACTION ON UPDATE NO ACTION, CONSTRAINT fk_PROCEDURE_ICD1 FOREIGN KEY (icd_code , icd_version)  REFERENCES clinicaldb.ICD (icd_code , icd_version) ON DELETE NO ACTION ON UPDATE NO ACTION) ENGINE = InnoDB"
cursor.execute(query)

#creating SERVICE table
query = "CREATE TABLE IF NOT EXISTS clinicaldb.SERVICE (subject_id INT NOT NULL, hospital_id VARCHAR(45) NOT NULL, transfertime DATETIME NOT NULL, prev_service VARCHAR(45) NULL, curr_service VARCHAR(45) NULL, PRIMARY KEY (subject_id, transfertime, hospital_id), INDEX fk_SERVICE_HOSPITAL1_idx (hospital_id ASC) VISIBLE, CONSTRAINT fk_SERVICE_SUBJECT1 FOREIGN KEY (subject_id) REFERENCES clinicaldb.SUBJECT (subject_id) ON DELETE NO ACTION ON UPDATE NO ACTION, CONSTRAINT fk_SERVICE_HOSPITAL1 FOREIGN KEY (hospital_id) REFERENCES clinicaldb.HOSPITAL (hospital_id) ON DELETE NO ACTION ON UPDATE NO ACTION) ENGINE = InnoDB"
cursor.execute(query)

#shows all tables in clinicaldb (was used for testing database initiation)
#query = "SHOW TABLES FROM clinicaldb"
#cursor.execute(query)
#print("Tables in clinicaldb:")
#for table in cursor:
#    print(f"{table}")

#sample query / print of results
#cursor.exec("SELECT * FROM SUBJECT WHERE gender='F'")
#for (subject_id, gender, age, year_group, date_of_death, marital_status, race, language) in cursor:
#    print(f"{subject_id}, {gender}, {age}, {year_group}, {date_of_death}, {marital_status}, {race}, {language}")

#cursor.execute("DROP DATABASE clinicaldb")

cursor.close()
con.close()

#previous connection was to server, this one is to connect to 'clinicaldb' itself
try:
    con = mariadb.connect(
        user="root",
        password="password",
        host="127.0.0.1",
        port=3306,
        database="clinicaldb"
    )

except mariadb.Error as e:
    print(f"Error connecting to MariaDB platform: {e}")
    sys.exit(1)

cursor = con.cursor()
cursor.execute("GRANT FILE ON *.* TO 'root'@'127.0.0.1'")

def enterAdmissionData(id, hid, admittime, dischtime, deathtime, adm_type, adm_prov, adm_loc, disch_loc, insurance_type, edregtime, edouttime, hosp_expire):
    if admittime == 'nan':
        admittime = pd.to_datetime('2000-01-01')
    try:
        pd.to_datetime(admittime)
    except:
        admittime = pd.to_datetime('2000-01-01')
    if dischtime == 'nan':
        dischtime = pd.to_datetime('2000-01-01')
    try:
        pd.to_datetime(dischtime)
    except:
        dischtime = pd.to_datetime('2000-01-01')
    if deathtime == 'nan':
        deathtime = pd.to_datetime('2000-01-01')
    try:
        pd.to_datetime(deathtime)
    except:
        deathtime = pd.to_datetime('2000-01-01')
    if edregtime == 'nan':
        edregtime = pd.to_datetime('2000-01-01')
    try:
        pd.to_datetime(edregtime)
    except:
        edregtime = pd.to_datetime('2000-01-01')
    if edouttime == 'nan':
        edouttime = pd.to_datetime('2000-01-01')
    try:
        pd.to_datetime(edouttime)
    except:
        edouttime = pd.to_datetime('2000-01-01')
    if hosp_expire != 0 or hosp_expire != 1:
        hosp_expire = 0
    query = f"INSERT IGNORE INTO ADMISSION(subject_id, hospital_id, admittime, dischtime, deathtime, admission_type, amit_provider_id, admission_location, discharge_location, insurance_type, edregtime, edouttime, hospital_expire_flag) VALUES('{id}', '{hid}', '{admittime}', '{dischtime}', '{deathtime}', '{adm_type}', '{adm_prov}', '{adm_loc}', '{disch_loc}', '{insurance_type}', '{edregtime}', '{edouttime}', '{hosp_expire}')"
    cursor.execute(query)
    
def enterDiagnosisData(id, hid, seq, icdc, icdv):
    query = f"INSERT IGNORE INTO DIAGNOSIS(subject_id, hospital_id, seq_num, icd_code, icd_version) VALUES('{id}', '{hid}', '{seq}', '{icdc}', '{icdv}')"
    cursor.execute(query)

def enterDrgData(id, hid, drg_type, drg_code, drg_sev, drg_mor, desc):
    if drg_sev == 'nan':
        drg_sev = 0
    if drg_mor == 'nan':
        drg_mor = 0
    desc = desc.replace("'", "")
    query = f"INSERT IGNORE INTO DRG(subject_id, hospital_id, drg_type, drg_code, drg_severity, drg_mortality, description) VALUES('{id}', '{hid}', '{drg_type}', '{drg_code}', '{drg_sev}', '{drg_mor}', '{desc}')"
    cursor.execute(query)

def enterHcpcsData(hcpcs, cat, longd, shortd):
    longd = longd.replace("'", "")
    shortd = shortd.replace("'", "")
    query = f"INSERT IGNORE INTO HCPCS(hcpcs_code, category, long_desc, short_desc) VALUES('{hcpcs}', '{cat}', '{longd}', '{shortd}')"
    cursor.execute(query)

def enterHcpcseventData(id, hid, chart, code, seq, desc):
    if chart == 'nan':
        chart = pd.to_datetime('2000-01-01')
    try:
        pd.to_datetime(chart)
    except:
        chart = pd.to_datetime('2000-01-01')
    desc = desc.replace("'", "")
    query = f"INSERT IGNORE INTO HCPCS_EVENT(subject_id, hospital_id, chartdate, hcpcs_code, seq_num, short_description) VALUES('{id}', '{hid}', '{chart}', '{code}', '{seq}', '{desc}')"
    cursor.execute(query)

def enterHospitalData(hid):
    query = f"INSERT IGNORE INTO HOSPITAL(hospital_id) VALUES('{hid}')"
    cursor.execute(query)

def enterIcdData(code, version, title):
    title = title.replace("'", "")
    query = f"INSERT IGNORE INTO ICD(icd_code, icd_version, title) VALUES('{code}', '{version}', '{title}')"
    cursor.execute(query)

def enterLabitemData(id, name, fluid, category):
    name = name.replace("'", "")
    query = f"INSERT IGNORE INTO LAB_ITEM(item_id, name, fluid, category) VALUES('{id}', '{name}', '{fluid}', '{category}')"
    cursor.execute(query)

def enterMicrobiologyeventData(mid, sid, hid, msid, opid, chart, siid, sdesc, testseq, storedate, tiid, testname, orgid, orgname, isonum, quantity, abid, abname, dtext, dcomp, dval, interpretation, comments):
    if chart == 'nan':
        chart = pd.to_datetime('2000-01-01')
    try:
        pd.to_datetime(chart)
    except:
        chart = pd.to_datetime('2000-01-01')
    if storedate == 'nan':
        storedate = pd.to_datetime('2000-01-01')
    try:
        pd.to_datetime(storedate)
    except:
        storedate = pd.to_datetime('2000-01-01')
    interpretation = interpretation.replace("'", "")
    comments = comments.replace("'", "")
    query = f"INSERT IGNORE INTO MICROBIOLOGY_EVENT(microevent_id, subject_id, hospital_id, microspecimen_id, order_provider_id, chartdate, spec_item_id, spec_type_desc, test_seq, storedate, test_item_id, test_name, org_item_id, org_name, isolate_num, quantity, ab_item_id, ab_name, dilution_text, dilution_comparison, dilution_value, interpretation, comments) VALUES('{mid}', '{sid}', '{hid}', '{msid}', '{opid}', '{chart}', '{siid}', '{sdesc}', '{testseq}', '{storedate}', '{tiid}', '{testname}', '{orgid}', '{orgname}', '{isonum}', '{quantity}', '{abid}', '{abname}', '{dtext}', '{dcomp}', '{dval}', '{interpretation}', '{comments}')"
    cursor.execute(query)

def enterOmrData(sid, chart, seq, rname, rval):
    if chart == 'nan':
        chart = pd.to_datetime('2000-01-01')
    try:
        pd.to_datetime(chart)
    except:
        chart = pd.to_datetime('2000-01-01')
    query = f"INSERT IGNORE INTO OMR(subject_id, chartdate, seq_num, result_name, result_value) VALUES('{sid}', '{chart}', '{seq}', '{rname}', '{rval}')"
    cursor.execute(query)

def enterProcedureData(sid, hid, seq, chart, code, version):
    if chart == 'nan':
        chart = pd.to_datetime('2000-01-01')
    try:
        pd.to_datetime(chart)
    except:
        chart = pd.to_datetime('2000-01-01')
    query = f"INSERT IGNORE INTO PROCEDURE_TABLE(subject_id, hospital_id, seq_num, chartdate, icd_code, icd_version) VALUES('{sid}', '{hid}', '{seq}', '{chart}', '{code}', '{version}')"
    cursor.execute(query)

def enterServiceData(sid, hid, transfertime, prev, curr):
    if transfertime == 'nan':
        transfertime = pd.to_datetime('2000-01-01')
    try:
        pd.to_datetime(transfertime)
    except:
        transfertime = pd.to_datetime('2000-01-01')
    query = f"INSERT IGNORE INTO SERVICE(subject_id, hospital_id, transfertime, prev_service, curr_service) VALUES('{sid}', '{hid}', '{transfertime}', '{prev}', '{curr}')"
    cursor.execute(query)

def enterSubjectData(id, gender, age, yeargrp, dod, marital, race, language):
    if dod == 'nan':
        dod = pd.to_datetime('2000-01-01')
    try:
        pd.to_datetime(dod)
    except:
        dod = pd.to_datetime('2000-01-01')
    query = f"INSERT IGNORE INTO SUBJECT(subject_id, gender, age, year_group, date_of_death, marital_status, race, language) VALUES ('{id}', '{gender}', '{age}', '{yeargrp}', '{dod}', '{marital}', '{race}', '{language}')"
    cursor.execute(query)

#updates SUBJECT entries w details from 'admissions.csv'
def updateSubjectData(id, marital, race, language):
    query = f"UPDATE SUBJECT SET marital_status = '{marital}', race = '{race}', language = '{language}' WHERE subject_id = '{id}'"
    cursor.execute(query)

#export ADMISSION table to .csv file
def exportAdmission():
    query = "SELECT * FROM ADMISSION INTO OUTFILE 'clinicaldb/output/admissions.csv' FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n'"
    cursor.execute(query)

#export DIAGNOSIS table to .csv file
def exportDiagnosis():
    query = "SELECT * FROM DIAGNOSIS INTO OUTFILE 'clinicaldb/output/diagnoses.csv' FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n'"
    cursor.execute(query)

#export DRG table to .csv file
def exportDrg():
    query = "SELECT * FROM DRG INTO OUTFILE 'clinicaldb/output/drgs.csv' FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n'"
    cursor.execute(query)

#export HCPCS table to .csv file
def exportHcpcs():
    query = "SELECT * FROM HCPCS INTO OUTFILE 'clinicaldb/output/hcpcs.csv' FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n'"
    cursor.execute(query)

#export HCPCS_EVENT table to .csv file
def exportHcpcsevent():
    query = "SELECT * FROM HCPCS_EVENT INTO OUTFILE 'clinicaldb/output/hcpcsevents.csv' FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n'"
    cursor.execute(query)

#export HOSPITAL table to .csv file
def exportHospital():
    query = "SELECT * FROM HOSPITAL INTO OUTFILE 'clinicaldb/output/hospitals.csv' FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n'"
    cursor.execute(query)

#export ICD table to .csv file
def exportIcd():
    query = "SELECT * FROM ICD INTO OUTFILE 'clinicaldb/output/icd.csv' FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n'"
    cursor.execute(query)

#export LAB_ITEM table to .csv file
def exportLabitem():
    query = "SELECT * FROM LAB_ITEM INTO OUTFILE 'clinicaldb/output/labitems.csv' FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n'"
    cursor.execute(query)

#export MICROBIOLOGY_EVENT table to .csv file
def exportMicrobiologyevent():
    query = "SELECT * FROM MICROBIOLOGY_EVENT INTO OUTFILE 'clinicaldb/output/microbiologyevents.csv' FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n'"
    cursor.execute(query)

#export OMR table to .csv file
def exportOmr():
    query = "SELECT * FROM OMR INTO OUTFILE 'clinicaldb/output/omr.csv' FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n'"
    cursor.execute(query)

#export PROCEDURE_TABLE table to .csv file
def exportProcedure():
    query = "SELECT * FROM PROCEDURE_TABLE INTO OUTFILE 'clinicaldb/output/procedures.csv' FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n'"
    cursor.execute(query)

#export SERVICE table to .csv file
def exportService():
    query = "SELECT * FROM SERVICE INTO OUTFILE 'clinicaldb/output/services.csv' FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n'"
    cursor.execute(query)

#export SUBJECT table to .csv file
def exportSubject():
    query = "SELECT * FROM SUBJECT INTO OUTFILE 'clinicaldb/output/subjects.csv' FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n'"
    cursor.execute(query)

#print rows from ADMISSION table
def printAdmission(n):
    query = f"SELECT * FROM ADMISSION FETCH FIRST {n} ROWS ONLY"
    cursor.execute(query)

    print(f"First {n} rows of ADMISSION:")
    for(subject_id, hospital_id, admittime, dischtime, deathtime, admission_type, amit_provider_id, admission_location, discharge_location, insurance_type, edregtime, edouttime, hospital_expire_flag) in cursor:
        print(f"{subject_id}, {hospital_id}, {admittime}, {dischtime}, {deathtime}, {admission_type}, {amit_provider_id}, {admission_location}, {discharge_location}, {insurance_type}, {edregtime}, {edouttime}, {hospital_expire_flag}")

#print rows from DIAGNOSIS table
def printDiagnosis(n):
    query = f"SELECT * FROM DIAGNOSIS FETCH FIRST {n} ROWS ONLY"
    cursor.execute(query)

    print(f"First {n} rows of DIAGNOSIS:")
    for(id, hid, seq, code, version) in cursor:
        print(f"{id}, {hid}, {seq}, {code}, {version}")

#print rows from DRG table
def printDrg(n):
    query = f"SELECT * FROM DRG FETCH FIRST {n} ROWS ONLY"
    cursor.execute(query)

    print(f"First {n} rows of DRG:")
    for(id, hid, drg_type, drg_code, drg_sev, drg_mor, desc) in cursor:
        print(f"{id}, {hid}, {drg_type}, {drg_code}, {drg_sev}, {drg_mor}, {desc}")

#print rows from HCPCS table
def printHcpcs(n):
    query = f"SELECT * FROM HCPCS FETCH FIRST {n} ROWS ONLY"
    cursor.execute(query)

    print(f"First {n} rows of HCPCS:")
    for(code, cat, longd, shortd) in cursor:
        print(f"{code}, {cat}, {longd}, {shortd}")

#print rows from HCPCS_EVENT table
def printHcpcsevent(n):
    query = f"SELECT * FROM HCPCS_EVENT FETCH FIRST {n} ROWS ONLY"
    cursor.execute(query)

    print(f"First {n} rows of HCPCS_EVENT:")
    for(id, hid, chart, code, seq, desc) in cursor:
        print(f"{id}, {hid}, {chart}, {code}, {seq}, {desc}")

#print rows from HOSPITAL table
def printHospital(n):
    query = f"SELECT * FROM HOSPITAL FETCH FIRST {n} ROWS ONLY"
    cursor.execute(query)

    print(f"First {n} rows of HOSPITAL:")
    for(hid) in cursor:
        print(f"{hid}")

#print rows from ICD table
def printIcd(n):
    query = f"SELECT * FROM ICD FETCH FIRST {n} ROWS ONLY"
    cursor.execute(query)

    print(f"First {n} rows of ICD:")
    for(icd_code, icd_version, title) in cursor:
        print(f"{icd_code}, {icd_version}, {title}")

#print rows from LAB_ITEM table
def printLabitem(n):
    query = (f"SELECT * FROM LAB_ITEM FETCH FIRST {n} ROWS ONLY")
    cursor.execute(query)

    print(f"First {n} rows of LAB_ITEM:")
    for(id, name, fluid, category) in cursor:
        print(f"{id}, {name}, {fluid}, {category}")

#print rows from MICROBIOLOGY_EVENT table
def printMicrobiologyevent(n):
    query = f"SELECT * FROM MICROBIOLOGY_EVENT FETCH FIRST {n} ROWS ONLY"
    cursor.execute(query)

    print(f"First {n} rows of MICROBIOLOGY_EVENT")
    for(mid, sid, hid, msid, opid, chart, siid, sdesc, testseq, storedate, tiid, testname, orgid, orgname, isonum, quantity, abid, abname, dtext, dcomp, dval, interpretation, comments) in cursor:
        print(f"{mid}, {sid}, {hid}, {msid}, {opid}, {chart}, {siid}, {sdesc}, {testseq}, {storedate}, {tiid}, {testname}, {orgid}, {orgname}, {isonum}, {quantity}, {abid}, {abname}, {dtext}, {dcomp}, {dval}, {interpretation}, {comments}")

#print rows from OMR table
def printOmr(n):
    query = f"SELECT * FROM OMR FETCH FIRST {n} ROWS ONLY"
    cursor.execute(query)

    print(f"First {n} rows of OMR:")
    for(sid, chart, seq, rname, rval) in cursor:
        print(f"{sid}, {chart}, {seq}, {rname}, {rval}")

#print rows from PRCEDURE_TABLE table
def printProcedure(n):
    query = f"SELECT * FROM PROCEDURE_TABLE FETCH FIRST {n} ROWS ONLY"
    cursor.execute(query)

    print(f"First {n} rows of PROCEDURE_TABLE:")
    for(sid, hid, seq, chart, code, version) in cursor:
        print(f"{sid}, {hid}, {seq}, {chart}, {code}, {version}")

#print rows from SERVICE table
def printService(n):
    query = f"SELECT * FROM SERVICE FETCH FIRST {n} ROWS ONLY"
    cursor.execute(query)

    print(f"First {n} rows of SERVICE:")
    for(sid, hid, transfertime, prev, curr) in cursor:
        print(f"{sid}, {hid}, {transfertime}, {prev}, {curr}")
        
#print rows from SUBJECT table
def printSubject(n):        
    query = f"SELECT * FROM SUBJECT FETCH FIRST {n} ROWS ONLY" 
    cursor.execute(query)

    print(f"First {n} rows of SUBJECT:")
    for (subject_id, gender, age, year_group, date_of_death, marital_status, race, language) in cursor:
        print(f"{subject_id}, {gender}, {age}, {year_group}, {date_of_death}, {marital_status}, {race}, {language}")


