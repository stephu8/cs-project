import React from 'react';
import FileUploader from './components/FileUpload/FileUploader'
import Header from './components/header/header';

const App = () => {
  return (
    <div className='body' style={{backgroundColor: '#ededdf'}}>
      <Header/>
      <h1>CSV File Upload</h1>
      <FileUploader />
    </div>
  );
};

export default App;
