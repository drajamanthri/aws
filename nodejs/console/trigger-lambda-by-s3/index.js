const aws = require('aws-sdk');
const s3 = new aws.S3({ apiVersion: '2006-03-01' });
const fs = require('fs');
const destinationBucket = 'test-dr-converted';
const path = require('path');

/**
 * This function is triggered by s3 object creation event.
 * It does the following tasks.
 * 1 Download the object. The object is expected to be a doc or docx file.
 * 2 Convert to pdf
 * 3 Upload to the destination bucket.
 * @param {*} event 
 * @returns 
 */
exports.handler = async (event) => {
    const sourceBucket = event.Records[0].s3.bucket.name;
    const key = event.Records[0].s3.object.key;
    const filename = path.parse(key).name;
    const downloadPath = '/tmp/' + key;

    console.log(sourceBucket, key);

    await download(sourceBucket, key, downloadPath);

    let file = fs.readFileSync(downloadPath);
    await upload(file, destinationBucket, key);
};

/**
 * This function downloads an object from a bucket. 
 * @param {string} bucket Download from bucket
 * @param {string} key Download object key
 * @param {string} downloadPath Download to path
 * @returns {Promise}
 */
async function download(bucket, key, downloadPath) {
    //s3.getObject returns AWS.Request which has promise() method.
    return s3.getObject({Bucket: bucket, Key: key})
    .promise()
    .then(
        function(file) {
            //save object in the download path
            fs.writeFileSync(downloadPath, file.Body);
            console.log('Download successful', key);
        }, 
        function(error) {
            console.log('Error downloading', key, error);
        }
    );
}

/**
 * This function uploads a local file to a s3 bucket
 * @param {Buffer} buffer 
 * @param {string} bucket uploading bucket
 * @param {string} key Uploading object key
 * @returns {Promise}
 */
async function upload(buffer, bucket, key) {
    //s3.putObject returns AWS.Request which has promise() method.
    return s3.putObject({
            Body: buffer,
            Key: key,
            Bucket: bucket
        })
    .promise(
        function() { 
            console.log('Uploading successful');
        }, 
        function(error) {
            console.log('Error uploading', key);
        }
    );
}
