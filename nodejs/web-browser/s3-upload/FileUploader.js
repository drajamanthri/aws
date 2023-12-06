import React from 'react';
import {useState} from 'react';
import axios from 'axios';


export default function FileUploader({uploadPolicyUrl}) {


   const [file, setFile] = useState(null);
   const handleFileChange = (e) => {
       const file = e.target.files[0];
       setFile(file);
   };


   /**
    * This function is used to retrieve pre-signed upload url synchronously.
    * @return {Promise}
    * promise result = {uploadUrl:string}
    */
   async function getUploadPolicy() {
       return fetch(uploadPolicyUrl, {
           headers: {
               "Content-Type": "application/json",
           }
       }).then(response => response.json());
   }


   const uploadFile = async () => {
       let data = await getUploadPolicy();


       let config = {
           onUploadProgress: function(progressEvent) {
               var percentCompleted = Math.round( (progressEvent.loaded * 100) / progressEvent.total );
               console.log('completed: ' + percentCompleted + '%');
           }
       };


       axios.put(data.uploadUrl, file, config)
       .then(function (res) {
           console.log('done');
       })
       .catch(function (err) {
           console.log('error');
       });
   };


   return (
       <div className="file-uploader">
           <div>
               <input type="file" onChange={handleFileChange} />
               <button onClick={uploadFile}>Upload</button>
           </div>
       </div>
   );
}
