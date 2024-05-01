############################################
#   Contains the functions to populate     #
#   clinicaldb                             #
############################################

#Creates meaningless entries to refer to avoid foreign key issues
def populateMeaningless():
    enterSubjectData(str(0), 'none', 'none', 'none', 'none', 'none', 'none', 'none')
    enterHcpcsData(str(0), 'none', 'does not exist', 'does not exist')
    enterHospitalData(str(0))
    enterIcdData(str(0), str(0), 'does not exist')
    enterLabitemData(str(0), 'does not exist', 'none', 'none')

#Calls all functions responsible for automatically populating clinicaldb with the Mimic dataset
def populateMimic():
    #populateHospitalMimic() - doesn't need to be called in current implementation (all .csv's with a hosp ID populate HOSPITAL while populating their respective tables)
    print("Populating clinicaldb with Mimic entries. Estimated duration: 5-6 hours")
    populateSubjectMimic()
    populateHcpcsMimic()
    populateIcdMimic()
    populateLabitemMimic()
    #Table above MUST be populated before tables below to avoid foreign key errors
    populateAdmissionMimic()
    populateDiagnosisMimic()
    populateDrgMimic()
    populateHcpcseventMimic()
    populateMicrobiologyeventMimic()
    populateOmrMimic()
    populateProcedureMimic()
    populateServiceMimic()

###Automatic population of clinicaldb using datasets other than Mimic - all col param are type string
##Independent tables (no foreign key constraints)
#Populates SUBJECT using param csv: the .csv being read, col1: column relating to subject_id, col2: column relating to gender, col3: column relating to age, col4: column relating to year_grp
#   col5: column relating to dod, col6: column relating to marital status, col7: column relating to race, col8: column relating to language
def populateSubject(csv, col1, col2, col3, col4, col5, col6, col7, col8):
    current = pd.read_csv(csv)
    for i in range(0, len(current)):
        if pd.isnull(col1):
            subject_id = None
        else:
            subject_id = str(current[col1].iloc[i])
            
        if pd.isnull(col2):
            gender = None
        else:
            gender = str(current[col2].iloc[i])
            
        if pd.isnull(col3):
            age = None
        else:
            age = str(current[col3].iloc[i])
            
        if pd.isnull(col4):
            year_grp = None
        else:
            year_grp = str(current[col4].iloc[i])
            
        if pd.isnull(col5):
            dod = None
        else:
            dod = str(current[col5].iloc[i])
            
        if pd.isnull(col6):
            marital = None
        else:
            marital = str(current[col6].iloc[i])
            
        if pd.isnull(col7):
            race = None
        else:
            race = str(current[col7].iloc[i])

        if pd.isnull(col8):
            language = None
        else:
            language = str(current[col8].iloc[i])
        print(f"Entry (sub) {i}: id - {subject_id}, gender - {gender}, age - {age}, year grp - {year_grp}, dod - {dod}, marital - {marital}, race - {race}, lan - {language}")
        enterSubjectData(subject_id, gender, age, year_grp, dod, marital, race, language)

#Populates HCPCS using param csv: the .csv being read, col1: column relating to hcpcs_code, col2: column relating to category, col3: column relating to long_description,
#   col4: column relating to short_description
def populateHcpcs(csv, col1, col2, col3, col4):
    current = pd.read_csv(csv)
    for i in range(0, len(current)):
        if pd.isnull(col1):
            code = None
        else:
            code = str(current[col1].iloc[i])
            
        if pd.isnull(col2):
            cat = None
        else:
            cat = str(current[col2].iloc[i])
            
        if pd.isnull(col3):
            longd = None
        else:
            longd = str(current[col3].iloc[i])
            
        if pd.isnull(col4):
            shortd = None
        else:
            shortd = str(current[col4].iloc[i])
        print(f"Entry (hcp) {i}: code - {code}, cat - {cat}, longd - {longd}, shortd - {shortd}")
        enterHcpcsData(code, cat, longd, shortd)

#Populates HOSPITAL using param csv: the .csv being read, col1: column relating to hospital_id
def populateHospital(csv, col1):
    current = pd.read_csv(csv)
    for i in range(0, len(current)):
        if pd.isnull(col1):
            hid = None
        else:
            hid = str(current[col1].iloc[i])
        print(f"Entry (hos) {i}: id - {hid}")
        enterHospitalData(hid)

#Populates ICD using param csv: the .csv being read, col1: column relating to icd_code, col2: column relating to icd_version, col3: column relating to title
def populateIcd(csv, col1, col2, col3):
    current = pd.read_csv(csv)
    for i in range(0, len(current)):
        if pd.isnull(col1):
            code = None
        else:
            code = str(current[col1].iloc[i])
            
        if pd.isnull(col2):
            version = None
        else:
            version = str(current[col2].iloc[i])
            
        if pd.isnull(col3):
            title = None
        else:
            title = str(current[col3].iloc[i])
        print(f"Entry (icd) {i}: code - {code}, ver - {version}, title - {title}")
        enterIcdData(code, version, title)

#Populates LAB_ITEM using param csv: the .csv being read, col1: column relating to id, col2: column relating to name, col3: column relating to fluid,
#   col4: column relating to category
def populateLabitem(csv, col1, col2, col3, col4):
    current = pd.read_csv(csv)
    for i in range(0, len(current)):
        if pd.isnull(col1):
            id = None
        else:
            id = str(current[col1].iloc[i])
            
        if pd.isnull(col2):
            name = None
        else:
            name = str(current[col2].iloc[i])
            
        if pd.isnull(col3):
            fluid = None
        else:
            fluid = str(current[col3].iloc[i])
            
        if pd.isnull(col4):
            cat = None
        else:
            cat = str(current[col4].iloc[i])
        print(f"Entry (lab) {i}: id - {id}, name - {name}, fluid - {fluid}, cat - {cat}")
        enterLabitemData(id, name, fluid, cat)

##Dependent tables (has foreign key contraints)
#Populates ADMISSION using param csv: the .csv being read, col1: column relating to subject_id, col2: column relating to hospital_id, col3: column relating to admittime
#   col4: column relating to disctime, col5: column relating to deathtime, col6: column relating to adm_type, col7: column relating to adm_prov, col8: column relating to adm_loc
#   col9: column relating to disch_loc, col10: column relating to insurance_type, col11: column relating to edregtime, col12: column relating to edouttime
#   col13: column relating to hospital_expire_flag
def populateAdmission(csv, col1, col2, col3, col4, col5, col6, col7, col8, col9, col10, col11, col12, col13):
    current = pd.read_csv(csv)
    for i in range(0, len(current)):
        if pd.isnull(col1):
            subject_id = 0
        else:
            subject_id = str(current[col1].iloc[i])
            
        if pd.isnull(col2):
            hid = 0
        else:
            hid = str(current[col2].iloc[i])
            
        if pd.isnull(col3):
            admit = None
        else:
            admit = str(current[col3].iloc[i])
            
        if pd.isnull(col4):
            disch = None
        else:
            disch = str(current[col4].iloc[i])
            
        if pd.isnull(col5):
            death = None
        else:
            death = str(current[col5].iloc[i])
            
        if pd.isnull(col6):
            adm_type = None
        else:
            adm_type = str(current[col6].iloc[i])
            
        if pd.isnull(col7):
            adm_prov = None
        else:
            adm_prov = str(current[col7].iloc[i])

        if pd.isnull(col8):
            adm_loc = None
        else:
            adm_loc = str(current[col8].iloc[i])

        if pd.isnull(col9):
            disch_loc = None
        else:
            disch_loc = str(current[col8].iloc[i])

        if pd.isnull(col10):
            ins_type = None
        else:
            ins_type = str(current[col8].iloc[i])

        if pd.isnull(col11):
            edreg = None
        else:
            edreg = str(current[col8].iloc[i])

        if pd.isnull(col12):
            edout = None
        else:
            edout = str(current[col8].iloc[i])

        if pd.isnull(col13):
            hef = None
        else:
            hef = str(current[col8].iloc[i])
        print(f"Entry (adm) {i}: id - {subject_id}, hid - {hid}, admit - {admit}, disc - {disch}, death - {death}, adm_type - {adm_type}, prov - {adm_prov}, loc - {adm_loc}, dloc - {disch_loc}, ins - {ins_type}, edreg - {edreg}, edout - {edout}, hef - {hef}")
        enterAdmissionData(subject_id, hid, admit, disch, death, adm_type, adm_prov, adm_loc, disch_loc, ins_type, edreg, edout, hef)

#Populates DIAGNOSIS using param csv: the .csv being read, col1: column relating to subject_id, col2: column relating to hospital_id, col3: column relating to seq_num,
#   col4: column relating to icd_code, col5: column relating to icd_version
def populateDiagnosis(csv, col1, col2, col3, col4, col5):
    current = pd.read_csv(csv)
    for i in range(0, len(current)):
        if pd.isnull(col1):
            sid = 0
        else:
            sid = str(current[col1].iloc[i])
            
        if pd.isnull(col2):
            hid = 0
        else:
            hid = str(current[col2].iloc[i])
            
        if pd.isnull(col3):
            seq = None
        else:
            seq = str(current[col3].iloc[i])
            
        if pd.isnull(col4):
            icdc = 0
        else:
            icdc = str(current[col4].iloc[i])

        if pd.isnull(col5):
            icdv = 0
        else:
            icdv = str(current[col5].iloc[i])
        print(f"Entry (dia) {i}: sid - {sid}, hid - {hid}, seq - {seq}, icdc - {icdc}, icdv - {icdv}")
        enterDiagnosisData(sid, hid, seq, icdc, icdv)

#Populates DRG using param csv: the .csv being read, col1: column relating to subject_id, col2: column relating to hospital_id, col3: column relating to drg_type,
#   col4: column relating to drg_code, col5: column relating to drg_sev, col6: column relating to drg_mor, col7: column relating to desc
def populateDrg(csv, col1, col2, col3, col4, col5, col6, col7):
    current = pd.read_csv(csv)
    for i in range(0, len(current)):
        if pd.isnull(col1):
            sid = 0
        else:
            sid = str(current[col1].iloc[i])
            
        if pd.isnull(col2):
            hid = 0
        else:
            hid = str(current[col2].iloc[i])
            
        if pd.isnull(col3):
            drg_type = None
        else:
            drg_type = str(current[col3].iloc[i])
            
        if pd.isnull(col4):
            code = None
        else:
            code = str(current[col4].iloc[i])

        if pd.isnull(col5):
            sev = None
        else:
            sev = str(current[col5].iloc[i])

        if pd.isnull(col6):
            mor = None
        else:
            mor = str(current[col6].iloc[i])

        if pd.isnull(col7):
            desc = None
        else:
            desc = str(current[col7].iloc[i])
        print(f"Entry (drg) {i}: sid - {sid}, hid - {hid}, type - {drg_type}, code - {code}, sev - {sev}, mor - {mor}, desc - {desc}")
        enterDrgData(sid, hid, drg_type, code, sev, mor, desc)

#Populates HCPCS_EVENT using param csv: the .csv being read, col1: column relating to subject_id, col2: column relating to hospital_id, col3: column relating to chartdate,
#   col4: column relating to hcpcs_code, col5: column relating to seq_num, col6: column relating to desc
def populateHcpcsevent(csv, col1, col2, col3, col4, col5, col6):
    current = pd.read_csv(csv)
    for i in range(0, len(current)):
        if pd.isnull(col1):
            sid = 0
        else:
            sid = str(current[col1].iloc[i])
            
        if pd.isnull(col2):
            hid = 0
        else:
            hid = str(current[col2].iloc[i])
            
        if pd.isnull(col3):
            chart = None
        else:
            chart = str(current[col3].iloc[i])
            
        if pd.isnull(col4):
            code = 0
        else:
            code = str(current[col4].iloc[i])

        if pd.isnull(col5):
            seq = None
        else:
            seq = str(current[col5].iloc[i])

        if pd.isnull(col6):
            desc = None
        else:
            desc = str(current[col6].iloc[i])
        print(f"Entry (hev) {i}: sid - {sid}, hid - {hid}, chart - {chart}, code - {code}, seq - {seq}, desc - {desc}")
        enterHcpcseventData(sid, hid, chart, code, seq, desc)

#Populates MICROBIOLOGY_EVENT using param csv: the .csv being read, col1: column relating to microevent_id, col2: column relating to subject_id, col3: column relating to hospital_id,
#   col4: column relating to microspecimen_id, col5: column relating to provider_id, col6: column relating to chartdate, col7: column relating to spec_item_id,
#   col8: column relating to spec_desc, col9: column relating to test_seq, col10: column relating to storedate, col11: column relating to test_item_id, col12: column relating to testname
#   col13: column relating to orgitem_id, col14: column relating to orgname, col15: column relating to isolate_num, col16: column relating to quantity, col17: column relating to abitem_id
#   col18: column relating to ab_name, col19: column relating to dilution_text, col20: column relating to dilution_comparison, col21: column relating to dilution_value
#   col22: column relating to interpretation, col23: column relating to comments
def populateMicrobiologyevent(csv, col1, col2, col3, col4, col5, col6, col7, col8, col9, col10, col11, col12, col13, col14, col15, col16, col17, col18, col19, col20, col21, col22, col23):
    current = pd.read_csv(csv)
    for i in range(0, len(current)):
        if pd.isnull(col1):
            mid = None
        else:
            mid = str(current[col1].iloc[i])
            
        if pd.isnull(col2):
            sid = 0
        else:
            sid = str(current[col2].iloc[i])
            
        if pd.isnull(col3):
            hid = 0
        else:
            hid = str(current[col3].iloc[i])
            
        if pd.isnull(col4):
            msid = None
        else:
            msid = str(current[col4].iloc[i])

        if pd.isnull(col5):
            opid = None
        else:
            opid = str(current[col5].iloc[i])

        if pd.isnull(col6):
            chart = None
        else:
            chart = str(current[col6].iloc[i])

        if pd.isnull(col7):
            siid = None
        else:
            siid = str(current[col7].iloc[i])

        if pd.isnull(col8):
            sdesc = None
        else:
            sdesc = str(current[col8].iloc[i])

        if pd.isnull(col9):
            testseq = None
        else:
            testseq = str(current[col9].iloc[i])

        if pd.isnull(col10):
            storedate = None
        else:
            storedate = str(current[col10].iloc[i])

        if pd.isnull(col11):
            tiid = None
        else:
            tiid = str(current[col11].iloc[i])

        if pd.isnull(col12):
            testname = None
        else:
            testname = str(current[col12].iloc[i])

        if pd.isnull(col13):
            orgid = None
        else:
            orgid = str(current[col13].iloc[i])

        if pd.isnull(col14):
            orgname = None
        else:
            orgname = str(current[col14].iloc[i])

        if pd.isnull(col15):
            isonum = None
        else:
            isonum = str(current[col15].iloc[i])

        if pd.isnull(col16):
            quantity = None
        else:
            quantity = str(current[col16].iloc[i])

        if pd.isnull(col17):
            abid = None
        else:
            abid = str(current[col17].iloc[i])

        if pd.isnull(col18):
            abname = None
        else:
            abname = str(current[col18].iloc[i])

        if pd.isnull(col19):
            dtext = None
        else:
            dtext = str(current[col19].iloc[i])

        if pd.isnull(col20):
            dcomp = None
        else:
            dcomp = str(current[col20].iloc[i])

        if pd.isnull(col21):
            dval = None
        else:
            dval = str(current[col21].iloc[i])

        if pd.isnull(col22):
            interpretation = None
        else:
            interpretation = str(current[col22].iloc[i])

        if pd.isnull(col23):
            comments = None
        else:
            comments = str(current[col23].iloc[i])
        print(f"Entry (mic) {i}")
        enterMicrobiologyeventData(mid, sid, hid, msid, opid, chart, siid, sdesc, testseq, storedate, tiid, testname, orgid, orgname, isonum, quantity, abid, abname, dtext, dcomp, dval, interpretation, comments)

#Populates OMR using param csv: the .csv being read, col1: column relating to subject_id, col2: column relating to chartdate, col3: column relating to seq_num,
#   col4: column relating to result_name, col5: column relating to result_value
def populateOmr(csv, col1, col2, col3, col4, col5):
    current = pd.read_csv(csv)
    for i in range(0, len(current)):
        if pd.isnull(col1):
            sid = 0
        else:
            sid = str(current[col1].iloc[i])
            
        if pd.isnull(col2):
            chart = None
        else:
            chart = str(current[col2].iloc[i])
            
        if pd.isnull(col3):
            seq = None
        else:
            seq = str(current[col3].iloc[i])
            
        if pd.isnull(col4):
            name = None
        else:
            name = str(current[col4].iloc[i])

        if pd.isnull(col5):
            value = None
        else:
            value = str(current[col5].iloc[i])
        print(f"Entry (omr) {i}: sid - {sid}, chart - {chart}, seq - {seq}, name - {name}, value - {value}")
        enterOmrData(sid, chart, seq, name, value)

#Populates PROCEDURE_TABLE using param csv: the .csv being read, col1: column relating to subject_id, col2: column relating to hospital_id, col3: column relating to seq_num,
#   col4: column relating to chartdate, col5: column relating to icd_code, col6: column relating to icd_version
def populateProcedure(csv, col1, col2, col3, col4, col5, col6):
    current = pd.read_csv(csv)
    for i in range(0, len(current)):
        if pd.isnull(col1):
            sid = 0
        else:
            sid = str(current[col1].iloc[i])
            
        if pd.isnull(col2):
            hid = 0
        else:
            hid = str(current[col2].iloc[i])
            
        if pd.isnull(col3):
            seq = None
        else:
            seq = str(current[col3].iloc[i])
            
        if pd.isnull(col4):
            chart = None
        else:
            chart = str(current[col4].iloc[i])

        if pd.isnull(col5):
            icdc = 0
        else:
            icdc = str(current[col5].iloc[i])

        if pd.isnull(col6):
            icdv = 0
        else:
            icdv = str(current[col6].iloc[i])
        print(f"Entry (pro) {i}: sid - {sid}, hid - {hid}, seq - {seq}, chart - {chart}, icdc - {icdc}, icdv - {icdv}")
        enterProcedureData(sid, hid, seq, chart, icdc, icdv)

#Populates OMR using param csv: the .csv being read, col1: column relating to subject_id, col2: column relating to hosptial_id, col3: column relating to transfertime,
#   col4: column relating to prev_service, col5: column relating to curr_service
def populateService(csv, col1, col2, col3, col4, col5):
    current = pd.read_csv(csv)
    for i in range(0, len(current)):
        if pd.isnull(col1):
            sid = 0
        else:
            sid = str(current[col1].iloc[i])
            
        if pd.isnull(col2):
            hid = 0
        else:
            hid = str(current[col2].iloc[i])
            
        if pd.isnull(col3):
            transfertime = None
        else:
            transfertime = str(current[col3].iloc[i])
            
        if pd.isnull(col4):
            prev = None
        else:
            prev = str(current[col4].iloc[i])

        if pd.isnull(col5):
            curr = None
        else:
            curr = str(current[col5].iloc[i])
        print(f"Entry (ser) {i}: sid - {sid}, hid - {hid}, time - {transfertime}, prev - {prev}, curr - {curr}")
        enterServiceData(sid, hid, transfertime, prev, curr)

###AUTOMATIC POPULATION OF clinicaldb FROM MIMIC DATASET
##Independent tables (no foreign key constraints) *HOSPITAL needs to be scraped from other Mimic csv's
#Scans 'patients.csv' and 'admissions.csv' to enter into SUBJECT table
def populateSubjectMimic():
    print("Populating SUBJECT with Mimic entries:")
    for x in range(0, len(mimic.files)-1):
        if compare_strings(mimic.files[x], "patients"):
            current = pd.read_csv(mimic.files[x])
            for i in range(0, len(current)):
                print(f"Entry {i}: id - {current.subject_id.iloc[i]}, gender - {current.gender.iloc[i]}, age - {current.anchor_age.iloc[i]}, year grp - {current.anchor_year_group.iloc[i]}, dod - {current.dod.iloc[i]}")
                enterSubjectData(str(current.subject_id.iloc[i]), str(current.gender.iloc[i]), str(current.anchor_age.iloc[i]), str(current.anchor_year_group.iloc[i]), str(current.dod.iloc[i]), None, None, None)
    print("")

#Scans 'd_hcpcs.csv' to enter into HCPCS table
def populateHcpcsMimic():
    print("Populating HCPCS with Mimic entries:")
    for x in range(0, len(mimic.files)-1):
        if compare_strings(mimic.files[x], "d_hcpcs"):
            current = pd.read_csv(mimic.files[x])
            for i in range(0, len(current)):
                print(f"Entering HCPCS {i}: code - {current.code.iloc[i]}, cat - {current.category.iloc[i]}, longd - {current.long_description.iloc[i]}, shortd - {current.short_description.iloc[i]}")
                enterHcpcsData(str(current.code.iloc[i]), str(current.category.iloc[i]), str(current.long_description.iloc[i]), str(current.short_description.iloc[i]))
    print("")

#Scans 'd_icd_diagnoses.csv' and 'd_icd_procedures.csv' to enter into ICD table
def populateIcdMimic():
    print("Populating ICD with Mimic entries:")
    for x in range(0, len(mimic.files)-1):
        if compare_strings(mimic.files[x], "d_icd_diagnoses"):
            current = pd.read_csv(mimic.files[x])
            for i in range(0, len(current)):
                print(f"Entry (diag) {i}: icd_code - {current.icd_code.iloc[i]}, icd_version - {current.icd_version.iloc[i]}, title - {current.long_title.iloc[i]}")
                enterIcdData(str(current.icd_code.iloc[i]), str(current.icd_version.iloc[i]), str(current.long_title.iloc[i]))
        if compare_strings(mimic.files[x], "d_icd_procedures"):
            current = pd.read_csv(mimic.files[x])
            for i in range(0, len(current)):
                print(f"Entry (proc) {i}: icd_code - {current.icd_code.iloc[i]}, icd_version - {current.icd_version.iloc[i]}, title - {current.long_title.iloc[i]}")
                enterIcdData(str(current.icd_code.iloc[i]), str(current.icd_version.iloc[i]), str(current.long_title.iloc[i]))
    print("")

#Scans 'd_labitems.csv' to enter into LAB_ITEM table
def populateLabitemMimic():
    print("Populating LAB_ITEM with Mimic entries:")
    for x in range(0, len(mimic.files)-1):
        if compare_strings(mimic.files[x], "d_labitems"):
            current = pd.read_csv(mimic.files[x])
            for i in range(0, len(current)):
                print(f"Entry {i}: id - {current.itemid.iloc[i]}, name - {current.label.iloc[i]}, fluid - {current.fluid.iloc[i]}, cat - {current.category.iloc[i]}")
                enterLabitemData(str(current.itemid.iloc[i]), str(current.label.iloc[i]), str(current.fluid.iloc[i]), str(current.category.iloc[i]))
    print("")

#Scans 'admissions.csv', 'diagnoses_icd.csv', 'drgcodes.csv', 'hcpcsevents.csv', 'microbiologyevents.csv', 'procedures_icd.csv', 'services.csv' to enter into HOSPITAL table
def populateHospitalMimic():
    print("Populating HOSPITAL with Mimic entries:")
    for x in range(0, len(mimic.files)):
        if compare_strings(mimic.files[x], "admission"):
            current = pd.read_csv(mimic.files[x])
            for i in range(0, len(current)):
                if pd.isnull(current.hadm_id.iloc[i]):
                    print(f"Entry (adm) {i}: No hospital_id")
                else:
                    print(f"Entry (adm) {i}: id - {current.hadm_id.iloc[i]}")
                    enterHospitalData(str(current.hadm_id.iloc[i]))
        elif compare_strings(mimic.files[x], "diagnoses_icd"):
            current = pd.read_csv(mimic.files[x])
            for i in range(0, len(current)):
                if pd.isnull(current.hadm_id.iloc[i]):
                    print(f"Entry (dia) {i}: No hospital_id")
                else:
                    print(f"Entry (dia) {i}: id - {current.hadm_id.iloc[i]}")
                    enterHospitalData(str(current.hadm_id.iloc[i]))
        elif compare_strings(mimic.files[x], "drgcodes"):
            current = pd.read_csv(mimic.files[x])
            for i in range(0, len(current)):
                if pd.isnull(current.hadm_id.iloc[i]):
                    print(f"Entry (drg) {i}: No hospital_id")
                else:
                    print(f"Entry (drg) {i}: id - {current.hadm_id.iloc[i]}")
                    enterHospitalData(str(current.hadm_id.iloc[i]))
        elif compare_strings(mimic.files[x], "hcpcsevents"):
            current = pd.read_csv(mimic.files[x])
            for i in range(0, len(current)):
                if pd.isnull(current.hadm_id.iloc[i]):
                    print(f"Entry (hcp) {i}: No hospital_id")
                else:
                    print(f"Entry (hcp) {i}: id - {current.hadm_id.iloc[i]}")
                    enterHospitalData(str(current.hadm_id.iloc[i]))
        elif compare_strings(mimic.files[x], "microbiology"):
            current = pd.read_csv(mimic.files[x])
            for i in range(0, len(current)):
                if pd.isnull(current.hadm_id.iloc[i]):
                    print(f"Entry (mic) {i}: No hospital_id")
                else:
                    print(f"Entry (mic) {i}: id - {current.hadm_id.iloc[i]}")
                    enterHospitalData(str(current.hadm_id.iloc[i]))
        elif compare_strings(mimic.files[x], "procedures_icd"):
            current = pd.read_csv(mimic.files[x])
            for i in range(0, len(current)):
                if pd.isnull(current.hadm_id.iloc[i]):
                    print(f"Entry (pro) {i}: No hospital_id")
                else:
                    print(f"Entry (pro) {i}: id - {current.hadm_id.iloc[i]}")
                    enterHospitalData(str(current.hadm_id.iloc[i]))
        elif compare_strings(mimic.files[x], "service"):
            current = pd.read_csv(mimic.files[x])
            for i in range(0, len(current)):
                if pd.isnull(current.hadm_id.iloc[i]):
                    print(f"Entry (ser) {i}: No hospital_id")
                else:
                    print(f"Entry (ser) {i}: id - {current.hadm_id.iloc[i]}")
                    enterHospitalData(str(current.hadm_id.iloc[i]))
    print("")

##Dependent tables (has foreign key restraints)
#Scans 'admissions.csv' to enter into ADMISSION table - see comments for preparation for implementation
def populateAdmissionMimic():
    print("Populating ADMISSION with Mimic entries:")
    for x in range(0, len(mimic.files)-1):
        if compare_strings(mimic.files[x], "admissions"):
            current = pd.read_csv(mimic.files[x])
            for i in range(0, len(current)):
                if pd.isnull(current.hadm_id.iloc[i]):                                                          
                    print(f"Entry (hos) {i}: No hospital_id")
                else:
                    print(f"Entry (hos) {i}: id - {current.hadm_id.iloc[i]}")
                    enterHospitalData(str(current.hadm_id.iloc[i]))    
                updateSubjectData(str(current.subject_id.iloc[i]), str(current.marital_status.iloc[i]), str(current.race.iloc[i]), str(current.language.iloc[i]))
                print(f"Entry {i}: id - {current.subject_id.iloc[i]}, hid - {current.hadm_id.iloc[i]}, admittime - {current.admittime.iloc[i]}, dischtime - {current.dischtime.iloc[i]}, deathtime - {current.deathtime.iloc[i]}, adm_type - {current.admission_type.iloc[i]}, adm_prov - {current.admit_provider_id.iloc[i]}, adm_loc - {current.admission_location.iloc[i]}, disch_loc - {current.discharge_location.iloc[i]}, ins_type - {current.insurance.iloc[i]}, edregtime - {current.edregtime.iloc[i]}, edouttime - {current.edouttime.iloc[i]}, hosp_ex - {current.hospital_expire_flag.iloc[i]}")
                enterAdmissionData(str(current.subject_id.iloc[i]), str(current.hadm_id.iloc[i]), str(current.admittime.iloc[i]), str(current.dischtime.iloc[i]), str(current.deathtime.iloc[i]), str(current.admission_type.iloc[i]), str(current.admit_provider_id.iloc[i]), str(current.admission_location.iloc[i]), str(current.discharge_location.iloc[i]), str(current.insurance.iloc[i]), str(current.edregtime.iloc[i]), str(current.edouttime.iloc[i]), str(current.hospital_expire_flag.iloc[i]))
    print("")

#Scans 'diagnoses.csv' to enter into DIAGNOSIS table - see comments for preparation for implementation
def populateDiagnosisMimic():
    print("Populating DIAGNOSIS with Mimic entries:")
    for x in range(0, len(mimic.files)-1):
        if compare_strings(mimic.files[x], "diagnoses_icd"):
            current = pd.read_csv(mimic.files[x])
            for i in range(0, len(current)):
                if pd.isnull(current.hadm_id.iloc[i]):                                                          
                    print(f"Entry (hos) {i}: No hospital_id")
                else:
                    print(f"Entry (hos) {i}: id - {current.hadm_id.iloc[i]}")
                    enterHospitalData(str(current.hadm_id.iloc[i]))
                print(f"Entry {i}: id - {current.subject_id.iloc[i]}, hid - {current.hadm_id.iloc[i]}, seqnum - {current.seq_num.iloc[i]}, icdc - {current.icd_code.iloc[i]}, icdv - {current.icd_version.iloc[i]}")
                enterDiagnosisData(str(current.subject_id.iloc[i]), str(current.hadm_id.iloc[i]), str(current.seq_num.iloc[i]), str(current.icd_code.iloc[i]), str(current.icd_version.iloc[i]))
    print("")

#Scans 'drg.csv' to enter into DRG table - see comments for preparation for implementation
def populateDrgMimic():
    print("Populating DRG with Mimic entries:")
    for x in range(0, len(mimic.files)-1):
        if compare_strings(mimic.files[x], "drg"):
            current = pd.read_csv(mimic.files[x])
            for i in range(0, len(current)):
                if pd.isnull(current.hadm_id.iloc[i]):                                                          
                    print(f"Entry (hos) {i}: No hospital_id")
                else:
                    print(f"Entry (hos) {i}: id - {current.hadm_id.iloc[i]}")
                    enterHospitalData(str(current.hadm_id.iloc[i]))              
                print(f"Entry {i}: id - {current.subject_id.iloc[i]}, hid - {current.hadm_id.iloc[i]}, type - {current.drg_type.iloc[i]}, code - {current.drg_code.iloc[i]}, sev - {current.drg_severity.iloc[i]}, mor - {current.drg_mortality.iloc[i]}, desc - {current.description.iloc[i]}")
                enterDrgData(str(current.subject_id.iloc[i]), str(current.hadm_id.iloc[i]), str(current.drg_type.iloc[i]), str(current.drg_code.iloc[i]), str(current.drg_severity.iloc[i]), str(current.drg_mortality.iloc[i]), str(current.description.iloc[i]))
    print("")                                                                                           

#Scans 'hcpcsevents.csv' to enter into HCPCS_EVENT table - see comments for preparation for implementation
def populateHcpcseventMimic():
    print("Populating HCPCS_EVENT with Mimic entries:")
    for x in range(0, len(mimic.files)-1):
        if compare_strings(mimic.files[x], "hcpcsevent"):
            current = pd.read_csv(mimic.files[x])
            for i in range(0, len(current)):
                if pd.isnull(current.hadm_id.iloc[i]):                                                          
                    print(f"Entry (hos) {i}: No hospital_id")
                else:
                    print(f"Entry (hos) {i}: id - {current.hadm_id.iloc[i]}")
                    enterHospitalData(str(current.hadm_id.iloc[i])) 
                print(f"Entry {i}: id - {current.subject_id.iloc[i]}, hid - {current.hadm_id.iloc[i]}, chart - {current.chartdate.iloc[i]}, code - {current.hcpcs_cd.iloc[i]}, seq - {current.seq_num.iloc[i]}, desc - {current.short_description.iloc[i]}")
                enterHcpcseventData(str(current.subject_id.iloc[i]), str(current.hadm_id.iloc[i]), str(current.chartdate.iloc[i]), str(current.hcpcs_cd.iloc[i]), str(current.seq_num.iloc[i]), str(current.short_description.iloc[i]))
    print("")

#Scans 'microbiologyevents.csv' to enter into MICROBIOLOGY_EVENT table - see comments for preparation for implementation
def populateMicrobiologyeventMimic():
    print("Populating MICROBIOLOGY_EVENT with Mimic entries:")
    for x in range(0, len(mimic.files)-1):
        if compare_strings(mimic.files[x], "microbiology"):
            current = pd.read_csv(mimic.files[x])
            for i in range(0, len(current)):
                if pd.isnull(current.hadm_id.iloc[i]):                                                          
                    print(f"Entry (hos) {i}: No hospital_id")
                    enterHospitalData(str(current.hadm_id.iloc[i]))
                else:
                    print(f"Entry (hos) {i}: id - {current.hadm_id.iloc[i]}")
                    enterHospitalData(str(current.hadm_id.iloc[i]))  
                print(f"Entry {i}: mid - {current.microevent_id.iloc[i]}, sid - {current.subject_id.iloc[i]}, hid - {current.hadm_id.iloc[i]}, msid - {current.micro_specimen_id.iloc[i]}, opid - {current.order_provider_id.iloc[i]}, chart - {current.charttime.iloc[i]}, siid - {current.spec_itemid.iloc[i]}, sdesc - {current.spec_type_desc.iloc[i]}, testseq - {current.test_seq.iloc[i]}, storedate - {current.storetime.iloc[i]}, tiid - {current.test_itemid.iloc[i]}, testname - {current.test_name.iloc[i]}, orgid - {current.org_itemid.iloc[i]}, orgname - {current.org_name.iloc[i]}, isonum - {current.isolate_num.iloc[i]}, quantity - {current.quantity.iloc[i]}, abid - {current.ab_itemid.iloc[i]}, abname - {current.ab_name.iloc[i]}, dtext - {current.dilution_text.iloc[i]}, dcomp - {current.dilution_comparison.iloc[i]}, dval - {current.dilution_value.iloc[i]}, interpretation - {current.interpretation.iloc[i]}, comments - {current.comments.iloc[i]}")
                enterMicrobiologyeventData(str(current.microevent_id.iloc[i]), str(current.subject_id.iloc[i]), str(current.hadm_id.iloc[i]), str(current.micro_specimen_id.iloc[i]), str(current.order_provider_id.iloc[i]), str(current.charttime.iloc[i]), str(current.spec_itemid.iloc[i]), str(current.spec_type_desc.iloc[i]), str(current.test_seq.iloc[i]), str(current.storetime.iloc[i]), str(current.test_itemid.iloc[i]), str(current.test_name.iloc[i]), str(current.org_itemid.iloc[i]), str(current.org_name.iloc[i]), str(current.isolate_num.iloc[i]), str(current.quantity.iloc[i]), str(current.ab_itemid.iloc[i]), str(current.ab_name.iloc[i]), str(current.dilution_text.iloc[i]), str(current.dilution_comparison.iloc[i]), str(current.dilution_value.iloc[i]), str(current.interpretation.iloc[i]), str(current.comments.iloc[i]))
    print("") 

#Scans 'omr.csv' to enter into OMR table - see comments for preparation for implementation
def populateOmrMimic():
    print("Populating OMR with Mimic entries:")
    for x in range(0, len(mimic.files)-1):
        if compare_strings(mimic.files[x], "omr"):
            current = pd.read_csv(mimic.files[x])
            for i in range(0, len(current)):
                print(f"Entry {i}: id - {current.subject_id.iloc[i]}, chart - {current.chartdate.iloc[i]}, seq - {current.seq_num.iloc[i]}, rname - {current.result_name.iloc[i]}, rval - {current.result_value.iloc[i]}")
                enterOmrData(str(current.subject_id.iloc[i]), str(current.chartdate.iloc[i]), str(current.seq_num.iloc[i]), str(current.result_name.iloc[i]), str(current.result_value.iloc[i]))
    print("") 

#Scans 'procedures_icd.csv' to enter into PROCEDURES table - see comments for preparation for implementation
def populateProcedureMimic():
    print("Populating PROCEDURE_TABLE with Mimic entries:")
    for x in range(0, len(mimic.files)-1):
        if compare_strings(mimic.files[x], "procedures_icd"):
            current = pd.read_csv(mimic.files[x])
            for i in range(0, len(current)):
                if pd.isnull(current.hadm_id.iloc[i]):                                                          
                    print(f"Entry (hos) {i}: No hospital_id")
                else:
                    print(f"Entry (hos) {i}: id - {current.hadm_id.iloc[i]}")
                    enterHospitalData(str(current.hadm_id.iloc[i]))                                             
                print(f"Entry {i}: id - {current.subject_id.iloc[i]}, hid - {current.hadm_id.iloc[i]}, seq - {current.seq_num.iloc[i]}, chart - {current.chartdate.iloc[i]}, code - {current.icd_code.iloc[i]}, ver - {current.icd_version.iloc[i]}")
                enterProcedureData(str(current.subject_id.iloc[i]), str(current.hadm_id.iloc[i]), str(current.seq_num.iloc[i]), str(current.chartdate.iloc[i]), str(current.icd_code.iloc[i]), str(current.icd_version.iloc[i]))                                            
    print("") 

#Scans 'services.csv' to enter into SERVICE table - see comments for preparation for implementation
def populateServiceMimic():
    print("Populating SERVICE with Mimic entries:")
    for x in range(0, len(mimic.files)):
        if compare_strings(mimic.files[x], "service"):
            current = pd.read_csv(mimic.files[x])
            for i in range(0, len(current)):                   
                if pd.isnull(current.hadm_id.iloc[i]):                                                          
                    print(f"Entry (hos) {i}: No hospital_id")
                else:
                    print(f"Entry (hos) {i}: id - {current.hadm_id.iloc[i]}")
                    enterHospitalData(str(current.hadm_id.iloc[i]))                                             
                print(f"Entry {i}: id - {current.subject_id.iloc[i]}, hid - {current.hadm_id.iloc[i]}, transfer - {current.transfertime.iloc[i]}, prev - {current.prev_service.iloc[i]}, curr - {current.curr_service.iloc[i]}")
                enterServiceData(str(current.subject_id.iloc[i]), str(current.hadm_id.iloc[i]), str(current.transfertime.iloc[i]), str(current.prev_service.iloc[i]), str(current.curr_service.iloc[i]))                                                                   
    print("")


    
