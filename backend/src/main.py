exec(open("./startup.py").read())
exec(open("./columninfo.py").read())
exec(open("./connector.py").read())
exec(open("./populator.py").read())
from flask import Flask, request, jsonify

############################################
#   This file executes previous files.     #
#   startup.py must be executed first in   #
#   order for following exec calls to      #
#   function correctly.                    #
############################################

# if savestate file is available then unpickle it
# prevents having to use to heavy processing several times
# USE WITH CAUTION - ONLY FOR TESTING
if os.path.isfile(STATEFILE ):
    SETS = pickle.load(open(STATEFILE, 'rb'))
    log(f'LOADED STATE FROM FILE {STATEFILE}')
else:
    SETS.append(SET(MIMICFILELOC))
    SETS.append(SET(CDCDEATHSFILELOC))
    pickle.dump(SETS, open(STATEFILE, 'wb'))
    log(f'SAVED STATE IN FILE {STATEFILE}')
# set
mimic=SETS[0]

#Need directory of csv to properly call all enter functions
def masterFunction(args = sys.argv):
    for i in range(0, len(args)):
        if args[i] == 'None':
            args[i] = None
    csv = args[2]
    match args[1]:
        case "Admission":
            populateAdmission(csv, args[3], args[4], args[5], args[6], args[7], args[8], args[9], args[10], args[11], args[12], args[13], args[14], args[15])
        case "Diagnosis":
            populateDiagnosis(csv, args[3], args[4], args[5], args[6], args[7])
        case "DRG":
            populateDrg(csv, args[3], args[4], args[5], args[6], args[7], args[8], args[9])
        case "HCPCS":
            populateHcpcs(csv, args[3], args[4], args[5], args[5])
        case "HCPCS_Event":
            populateHcpcsevent(csv, args[3], args[4], args[5], args[6], args[7], args[8])
        case "Hospital":
            populateHospital(csv, args[3])
        case "ICD":
            populateIcd(csv, args[3], args[4], args[5])
        case "Lab_Item":
            populateLabitem(csv, args[3], args[4], args[5], args[6])
        case "Microbiology_Event":
            populateMicrobiologyevent(csv, args[3], args[4], args[5], args[6], args[7], args[8], args[9], args[10], args[11], args[12], args[13], args[14], args[15], args[16], args[17], args[18], args[19], args[20], args[21], args[22], args[23], args[24], args[25])
        case "OMR":
            populateOmr(csv, args[3], args[4], args[5], args[6], args[7])
        case "Procedure":
            populateProcedure(csv, args[3], args[4], args[5], args[6], args[7], args[8])
        case "Service":
            populateService(csv, args[3], args[4], args[5], args[6], args[7])
        case "Subject":
            populateSubject(csv, args[3], args[4], args[5], args[6], args[7], args[8], args[9], args[10])

"""
###Flask server
##Creating flask server
app = Flask(__name__)

##API routes for flask server
@app.route("/")
def test():
    return "Welcome to the API"

@app.route("/tables")
def tables():
    data = ["Admission", "Diagnosis", "DRG", "HCPCS", "HCPCS_Event", "Hospital", "ICD", "Lab_item", "Microbiology_Event", "OMR", "Procedure", "Service", "Subject"]
    return jsonify(data), 200

#Admission routes
@app.route("/Admissionget", methods=["GET"])
def admissionget():
    data = ["subject_id", "hospital_id", "admittime", "dischtime", "deathtime", "admission_type", "admit_provider_id", "admission_location", "discharge_location", "insurance", "edregtime", "edouttime", "hospital_expire_flag"]
    return jsonify(data), 200

@app.route("/Admissionpost", methods=["POST"])
def admissionpost():
    data = request.get_json()
    #enter data into db
    return "Success", 201

#Diagnosis routes
@app.route("/Diagnosisget", methods=["GET"])
def diagnosisget():
    data = ["subject_id", "hospital_id", "seq_num", "icd_code", "icd_version"]
    return jsonify(data), 200

@app.route("/Diagnosispost", methods=["POST"])
def diagnosispost():
    data = request.get_json()
    #enter data into db
    return "Success", 201

#DRG routes
@app.route("/DRGget", methods=["GET"])
def drgget():
    data = ["subject_id", "hospital_id", "drg_type", "drg_code", "drg_severity", "drg_mortality", "description"]
    return jsonify(data), 200

@app.route("/DRGpost", methods=["POST"])
def drgpost():
    data = request.get_json()
    #enter data into db
    return "Success", 201

#HCPCS routes
@app.route("/HCPCSget", methods=["GET"])
def hcpcsget():
    data = ["hcpcs_code", "category", "long_description", "short_description"]
    return jsonify(data), 200

@app.route("/HCPCSpost", methods=["POST"])
def hcpcspost():
    data = request.get_json()
    #enter data into db
    return "Success", 201

#HCPCS Event routes
@app.route("/HCPCS_Eventget", methods=["GET"])
def hcpcseventget():
    data = ["subject_id", "hospital_id", "chartdate", "hcpcs_code", "seq_num", "short_description"]
    return jsonify(data), 200

@app.route("/HCPCS_Eventpost", methods=["POST"])
def hcpcseventpost():
    data = request.get_json()
    #enter data into db
    return "Success", 201

#Hospital routes
@app.route("/Hospitalget", methods=["GET"])
def hospitalget():
    data = ["hospital_id"]
    return jsonify(data), 200

@app.route("/Hospitalpost", methods=["POST"])
def hospitalpost():
    data = request.get_json()
    #enter data into db
    return "Success", 201

#ICD routes
@app.route("/ICDget", methods=["GET"])
def icdget():
    data = ["icd_code", "icd_version", "title"]
    return jsonify(data), 200

@app.route("/ICDpost", methods=["POST"])
def icdpost():
    data = request.get_json()
    #enter data into db
    return "Success", 201

#Lab Item routes
@app.route("/Lab_Itemget", methods=["GET"])
def labitemget():
    data = ["item_id", "label", "fluid", "category"]
    return jsonify(data), 200

@app.route("/Lab_Itempost", methods=["POST"])
def labitempost():
    data = request.get_json()
    #enter data into db
    return "Success", 201

#Microbiology Event routes
@app.route("/Microbiology_Eventget", methods=["GET"])
def microbiologyeventget():
    data = ["microevent_id", "subject_id", "hospital_id", "micro_specimen_id", "order_provider_id", "charttime", "spec_itemid", "spec_type_desc", "test_seq", "storetime", "test_itemid", "test_name", "org_itemid", "org_name", "isolate_num", "quantity", "ab_itemid", "ab_name", "dilution_text", "dilution_comparison", "dilution_value", "interpretation", "comments"]
    return jsonify(data), 200

@app.route("/Microbiology_Eventpost", methods=["POST"])
def microbiologyeventpost():
    data = request.get_json()
    #enter data into db
    return "Success", 201

#OMR routes
@app.route("/OMRget", methods=["GET"])
def omrget():
    data = ["subject_id", "chartdate", "seq_num", "result_name", "result_value"]
    return jsonify(data), 200

@app.route("/OMRpost", methods=["POST"])
def omrpost():
    data = request.get_json()
    #enter data into db
    return "Success", 201

#Procedure routes
@app.route("/Procedureget", methods=["GET"])
def procedureget():
    data = ["subject_id", "hospital_id", "seq_num", "chartdate", "icd_code", "icd_version"]
    return jsonify(data), 200

@app.route("/Procedurepost", methods=["POST"])
def procedurepost():
    data = request.get_json()
    #enter data into db
    return "Success", 201

#Service routes
@app.route("/Serviceget", methods=["GET"])
def serviceget():
    data = ["subject_id", "hospital_id", "transfertime", "prev_service", "curr_service"]
    return jsonify(data), 200

@app.route("/Servicepost", methods=["POST"])
def servicepost():
    data = request.get_json()
    #enter data into db
    return "Success", 201

#Subject routes
@app.route("/Subjectget", methods=["GET"])
def subjectget():
    data = ["subject_id", "gender", "age", "year_group", "dod", "race", "marital status", "language"]
    return jsonify(data), 200

@app.route("/Subjectpost", methods=["POST"])
def subjectpost():
    data = request.get_json()
    #enter data into db
    return "Success", 201

#Create an instance of the flask server
if __name__ == "__main__":
    app.run(debug=True)
"""

###POPULATING clinicaldb USING MIMIC
#populateMimic()

###POPULATING clinicaldb USING OTHER CSVs
populateMeaningless()   #used to avoid foreign key errors

##Testing export of db tables as .csvs
#populateSubject(mimic.files[0], "subject_id", "gender", "anchor_age", "anchor_year_group", "dod", None, None, None)
#exportSubject()

##Testing general populate functions with Mimic dataset
"""
populateSubject(mimic.files[0], "subject_id", "gender", "anchor_age", "anchor_year_group", "dod", None, None, None)
populateHcpcs(mimic.files[9], "code", "category", "long_description", "short_description")
populateIcd(mimic.files[6], "icd_code", "icd_version", "long_title")
populateHospital(mimic.files[7], "hadm_id")
populateLabitem(mimic.files[3], "itemid", "label", "fluid", "category")
populateAdmission(mimic.files[7], "subject_id", "hadm_id", "admittime", "dischtime", "deathtime", "admission_type", "admit_provider_id", "admission_location", "discharge_location", "insurance", "edregtime", "edouttime", "hospital_expire_flag")
populateDiagnosis(mimic.files[4], "subject_id", "hadm_id", "seq_num", "icd_code", "icd_version")
populateDrg(mimic.files[11], "subject_id", "hadm_id", "drg_type", "drg_code", "drg_severity", "drg_mortality", "description")
populateHcpcsevent(mimic.files[12], "subject_id", "hadm_id", "chartdate", "hcpcs_cd", "seq_num", "short_description")
populateMicrobiologyevent(mimic.files[2], "microevent_id", "subject_id", "hadm_id", "micro_specimen_id", "order_provider_id", "charttime", "spec_itemid", "spec_type_desc", "test_seq", "storetime", "test_itemid", "test_name", "org_itemid", "org_name", "isolate_num", "quantity", "ab_itemid", "ab_name", "dilution_text", "dilution_comparison", "dilution_value", "interpretation", "comments")
populateOmr(mimic.files[10], "subject_id", "chartdate", "seq_num", "result_name", "result_value")
populateProcedure(mimic.files[1], "subject_id", "hadm_id", "seq_num", "chartdate", "icd_code", "icd_version")
populateService(mimic.files[13], "subject_id", "hadm_id", "transfertime", "prev_service", "curr_service")
"""

## Code below produces errors
"""
# merging mimic
mergedset = pd.read_csv(mimic.files[0])
for x in range(1, len(mimic.files)-1):
    current = pd.read_csv(mimic.files[x])
    if colhasmatch(mergedset.columns, mimic.cols[x]) == True:
        mergedset = mergedset.merge(current)
    else:
        mergedset = pd.concat([mergedset, current], axis=1)
"""

























