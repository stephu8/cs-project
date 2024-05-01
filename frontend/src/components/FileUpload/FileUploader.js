import React, { useState } from 'react';
import './FileUpload.css';
import DatabaseDropdown from '../DatabaseDropdown/DatabaseDropdown';

const FileUploader = () => {
  const [columnsFile1, setColumnsFile1] = useState([]);
  const [selectedColumnsFile1, setSelectedColumnsFile1] = useState([]);
  const [file1Data, setFile1Data] = useState([]);
  const [selectedTable, setSelectedTable] = useState('');
  const [showTableDropdown, setShowTableDropdown] = useState(false);
  const [tableColumns, setTableColumns] = useState([]);


  //Function to call backend endpoint
  const runPythonScript = async () =>{
    const mimicTable = selectedTable; // Table selected from dropdown
    const csvPath = 'file1.csv'; // Path to merged CSV file
    const selectedColumns = selectedColumnsFile1; // Columns selected from file 1

    try{
      const response = await fetch('http://localhost:3000/run-python', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          mimicTable, 
          csvPath, 
          selectedColumns 
        }),
      });

      if(response.ok){
        const result = await response.text();
        console.log('Python script executed successfully:', result);
      } else {
        console.error('Error executing script');
      }
    } catch(error){
      console.error('Error executing script:', error);
    }
};

  //Event handler for calling the backend script
  const handleRunScript = () => {
    runPythonScript(); //Call the function when needed
  };

  const tables = [
    'Admissions', 
    'Hcpcs', 
    'ICD', 
    'ICD', 
    'Lab_items', 
    'Diagnoses', 
    'DRG', 
    'HCPCS_Events', 
    'Microbiology_event',
    'OMR',
    'Subject',
    'Procedure',
    'Service'
  ];

  // Define columns for each table
  const tableColumnsMap = {
    Admissions: ['subject_id', 'hospital_id', 'admittime', 'dischtime', 'deathtime', 'admission_type', 'admit_provider_id', 'admission_location', 'discharge_location', 'insurance', 'edregtime', 'edouttime', 'hospital_expire_flag'],
    Hcpcs: ['hcpcs_code', 'category', 'long_description', 'short_description'],
    ICD: ['icd_code', 'icd_version', 'long_title'],
    Lab_items: ['itemid', 'label', 'fluid', 'category'],
    Diagnoses: ['subject_id', 'hospital_id', 'seq_num', 'icd_code', 'icd_version'],
    DRG: ['subject_id', 'hospital_id', 'drg_type', 'drg_code', 'description', 'drg_severity', 'drg_mortality'],
    HCPCS_Events: ['subject_id', 'hospital_id', 'chartdate', 'hcpcs_cd', 'seq_num', 'short_description'],
    Microbiology_event: ['microevent_id', 'subject_id', 'hospital_id', 'micro_specimen_id', 'order_provider_id', 'chartdate', 'spec_itemid', 'spec_type_desc', 'test_seq', 'storedate', 'test_itemid', 'test_name', 'org_itemid', 'org_name', 'isolate_num', 'quantity', 'ab_itemid', 'ab_name', 'dilution_text', 'dilution_comparison', 'dilution_value', 'interpretation', 'comments'],
    OMR: ['subject_id', 'chartdate', 'seq_num', 'result_name', 'result_value'],
    Subject: ['subject_id', 'gender', 'anchor_age', 'year_group', 'dod', 'marital_status', 'race', 'language'],
    Procedure: ['subject_id', 'hospital_id', 'seq_num', 'chartdate', 'icd_code', 'icd_version'],
    Service: ['subject_id', 'hospital_id', 'transfertime', 'prev_service', 'curr_service']
  };

  const handleFileUpload = (event, fileNumber) => {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        const csv = e.target.result;
        const lines = csv.split('\n');
        if (lines.length > 0) {
          const header = lines[0].split(',');
          if (fileNumber === 1) {
            setColumnsFile1(header);
            setFile1Data(lines.slice(1).map(line => line.split(','))); // Skip header and parse data
            setSelectedColumnsFile1(header.slice(0, 3)); // Default selection of first 3 columns
            runPythonScript();
          }
        }
      };
      reader.readAsText(file);
    }
  };

  const handleTableSelect = (tableName) => {
    setSelectedTable(tableName);
    setTableColumns(tableColumnsMap[tableName] || []);
  };

  const handleColumnDropdownChange = (event, index) => {
    const { value } = event.target;
    setSelectedColumnsFile1(prevSelected => {
      const newSelected = [...prevSelected];
      newSelected[index] = value;
      return newSelected;
    });
  };

  const handleCheckboxChange = (event, columnName) => {
    const isChecked = event.target.checked;
    setSelectedColumnsFile1(prevSelected => {
      if (isChecked) {
        return [...prevSelected, columnName];
      } else {
        return prevSelected.filter(col => col !== columnName);
      }
    });
  };

  const handleCreateMergedCSV = () => {
    // Combine selected columns from both file and selected table
    const mergedColumns = [...selectedColumnsFile1];
  
    // Add selected table columns to mergedColumns if a table is selected
    if (selectedTable !== '') {
      switch (selectedTable) {
        case 'Admission':
          mergedColumns.push('subject_id', 'hospital_id', 'admittime', 'dischtime', 'deathtime', 'admission_type', 'admit_provider_id', 'admission_location', 'discharge_location', 'insurance', 'edregtime', 'edouttime', 'hospital_expire_flag');
          break;
        case 'Diagnosis':
          mergedColumns.push('subject_id','hospital_id','seq_num','icd_code','icd_version');
          break;
        case 'DRG':
          mergedColumns.push('subject_id','hospital_id','drg_type','drg_code','drg_severity','drg_mortality','description');
          break;
        case 'HCPCS':
          mergedColumns.push('hcpcs_code', 'category', 'long_description', 'short_description');
          break;
        case 'HCPCS_Event':
          mergedColumns.push('subject_id','hospital_id','chartdate','hcpcs_cd','seq_num','short_description');
          break;
        case 'Hospital':
          mergedColumns.push('hospital_id');
          break;
        case 'ICD':
          mergedColumns.push('icd_code','icd_version','long_title');
          break;
        case 'Lab_Item':
          mergedColumns.push('itemid','label','fluid','category');
          break;
        case 'Microbiology_Event':
          mergedColumns.push('microevent_id','subject_id','hospital_id','micro_specimen_id','order_provider_id','chartdate','spec_itemid','spec_type_desc','test_seq','storedate','test_itemid','test_name','org_itemid','org_name','isolate_num','quantity','ab_itemid','ab_name','dilution_text','dilution_comparison','dilution_value','interpretation','comments');
          break;
        case 'OMR':
          mergedColumns.push('subject_id','chartdate','seq_num','result_name','result_value');
          break;
        case 'Procedure':
          mergedColumns.push('subject_id','hospital_id','seq_num','chartdate','icd_code','icd_version');
          break;
        case 'Service':
          mergedColumns.push('subject_id','hospital_id','transfertime','prev_service','curr_service');
          break;
        case 'Subject':
          mergedColumns.push('subject_id','gender','anchor_age','year_group','dod', 'marital_status', 'race', 'language');
          break;
        default:
          break;
      }
    }
  
    // Combine data from the uploaded file based on merged columns
    const mergedData = [
      mergedColumns.join(','), // Add header row
      ...file1Data.map(row => {
        const rowData = mergedColumns.map(col =>
          selectedColumnsFile1.includes(col) ? row[columnsFile1.indexOf(col)] : ''
        );
        return rowData.join(',');
      }), // Add data from file 1
    ];
  
    // Create CSV content with merged data
    let csvContent = mergedData.join('\n');
  
    // Create Blob and download as CSV file
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', 'merged_file.csv');
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };
  


  return (
    <div className='body'>
      <div className="file-upload-container">
        {/* Table Selection */}
        <div className="box table-select-box">
          <button onClick={() => setShowTableDropdown(!showTableDropdown)}>Select Table</button>
          {showTableDropdown && (
            <select value={selectedTable} onChange={e => handleTableSelect(e.target.value)}>
              <option value="">Select Table</option>
              {tables.map(table => (
                <option key={table} value={table}>{table}</option>
              ))}
            </select>
          )}
          {selectedTable && (
                <div>
                  <h3>{selectedTable} Columns:</h3>
                  {tableColumns.map((col, index) => (
                <div key={index} className="column-checkbox">
                  <input
                    type="checkbox"
                    id={`${selectedTable}-${col}`}
                    checked={selectedColumnsFile1.includes(col)}
                    onChange={e => handleCheckboxChange(e, col)}
                  />
                  <label htmlFor={`${selectedTable}-${col}`}>{col}</label>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Left Box - File 1 Upload */}
        <div className="box left-box">
          <label htmlFor="file1">Upload CSV File 1</label> <br/>
          <input
            type="file"
            id="file1"
            accept=".csv"
            onChange={e => handleFileUpload(e, 1)}
          />
          <div className="column-dropdowns">
            <h2>File 1 Columns:</h2>
            {columnsFile1.map((column, index) => (
              <div key={index} className="column-dropdown">
                <select
                   value={selectedColumnsFile1[index] || ''}
                   onChange={e => handleColumnDropdownChange(e, index)}
                 >
                   <option value="">Select Column</option>
                   {columnsFile1.map((col, idx) => (
                     <option key={idx} value={col}>{col}</option>
                   ))}
                 </select>
               </div>
             ))}
           </div>
         </div>
      </div>

      <div className='center-master-div'>
        <button className='merge-button' onClick={handleCreateMergedCSV}>Create Merged CSV</button>
      </div>
    </div>
  );
};

export default FileUploader;