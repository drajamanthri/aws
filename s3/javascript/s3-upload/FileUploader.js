import React from 'react';
import { useState } from 'react';
import axios from 'axios';
import AWS from 'aws-sdk';

/**
 * 
 * @param {{startUrl:string, completeUrl:string}} param0 
 * When upload is started, a request is sent to the startUrl. The result of the start request depends on 
 * the environment.
 * production
 * {uploadUrl:string, env:'production'}
 * 
 * local
 * {env:local}
 * 
 * In the production environment, the file is uploaded using a pre-signed url
 * In the local environment (localstack), the file is uploaded using aws sdk for js.
 * @returns 
 */
export default function FileUploader({ startUrl, completeUrl }) {


    const [file, setFile] = useState(null);
    const handleFileChange = (e) => {
        const file = e.target.files[0];
        setFile(file);
    };


    /**
     * This function is used to retrieve pre-signed upload url synchronously.
     * @return {Promise}
     * promise result = {uploadUrl:string, env:string}
     * env: production or local
     */
    async function start() {
        return fetch(startUrl, {
            headers: {
                "Content-Type": "application/json",
            }
        }).then(response => response.json());
    }

    /**
     * This function notifies the server that the upload was completed.
     */
    async function complete() {
        fetch(completeUrl).
        then(response => {
            console.log('upload completed');
        });
    }


    /**
     * This function uploads a file. 
     * production env: upload using pre-signed url
     * local evn: upload using aws sdk for js.
     * 
     */
    const uploadFile = async () => {
        let configuration = await start();


        let config = {
            onUploadProgress: function (progressEvent) {
                var percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
                console.log('completed: ' + percentCompleted + '%');
            }
        };

        if (configuration.env == 'production') {
            //in the production environment, upload with pre-signed url
            axios.put(configuration.uploadUrl, file, config)
                .then(function (res) {
                    complete();
                })
                .catch(function (err) {
                    console.log('error');
                });
        } else {
            uploadLocal(configuration);
        }
    };

    /**
     * In the local environment, we would use localstack s3. Therefore, upload with pre-signed url is not 
     * necessary.
     * @param {{Bucket:string, Key:string, env:'local'}} configuration 
     */
    const uploadLocal = async (configuration) => {
        const s3 = new AWS.S3({
            endpoint: 'http://localhost:4566',
            region: 'us-west-1',
            accessKeyId: "test",
            secretAccessKey: "test",
            s3ForcePathStyle: true,
        });

        const params = {
            Bucket: configuration.Bucket,
            Key: configuration.Key,
            Body: file,
        };

        let upload = s3
            .putObject(params)
            .on("httpUploadProgress", (evt) => {
                let progress = parseInt((evt.loaded * 100) / evt.total);
                console.log(progress + '%');
            })
            .promise();

        upload.then(function () {
            complete();
        });
    }


    return (
        <div className="file-uploader">
            <div>
                <input type="file" onChange={handleFileChange} />
                <button onClick={uploadFile}>Upload</button>
            </div>
        </div>
    );
}
