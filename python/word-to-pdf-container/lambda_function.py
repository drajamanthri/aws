'''
references
subprocess
https://docs.python.org/3/library/subprocess.html
https://www.datacamp.com/tutorial/python-subprocess

libreoffice
https://wiki.documentfoundation.org/Documentation/Install/Linux
'''

import os
import boto3
import subprocess

upload_bucket = 'destination-bucket'

 
'''
This function downloads an object from s3 bucket
parameters
----------
bucket : string
    download bucket name
key : string
    object key
download_path : string
'''
def download_from_s3(bucket, key, download_path):
    s3 = boto3.client("s3")
    s3.download_file(bucket, key, download_path)
    
'''
This function uploads a file to s3
parameters
----------
file_path : string 
    upload file path 
bucket : string
    upload bucket name
key : string
    upload object key
'''
def upload_to_s3(file_path, bucket, key):
    s3 = boto3.client("s3")
    s3.upload_file(file_path, bucket, key)
    
'''
This function converts a doc file to pdf
soffice_path : string 
    libreoffice file path
word_file_path : string
    Input word file path
output_dir : string
'''
def convert_word_to_pdf(word_file_path, output_dir):
    conv_cmd = f"libreoffice7.6 --headless --invisible --nodefault --view --nolockcheck --nologo --norestore --convert-to pdf --outdir {output_dir} {word_file_path}"

    response = subprocess.run(conv_cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if response.returncode != 0:
        return False
    return True

def handler(event, context):
    #bucket = bucket name that triggered the event
    bucket = event['Records'][0]['s3']['bucket']['name']
    #key: test.docx
    key = event['Records'][0]['s3']['object']['key']
    print('src bucket', bucket, 'key', key)

    #key_prefix: ''
    #base_name: test.docx
    key_prefix, base_name = os.path.split(key)
    #download_path = s3 object download path
    download_path = f"/tmp/{base_name}"
    #output_dir = pdf file output path
    output_dir = "/tmp"
    file_name, ext = os.path.splitext(base_name)
    
    download_from_s3(bucket, key, download_path)
    if (os.path.exists(download_path)):
        print('pdf downloaded at ' + download_path)
    else:
        print('pdf was not downloaded at ' + download_path)

    is_converted = convert_word_to_pdf(download_path, output_dir)
    if (os.path.exists(f"{output_dir}/{file_name}.pdf")):
        print('pdf generated at ' + f"{output_dir}/{file_name}.pdf")
    else:
        print('pdf is NOT generated at ' + f"{output_dir}/{file_name}.pdf")

    if is_converted:
        #file_name: test
        #ext: .docx
        
        upload_key = ''
        if key_prefix:
            upload_key = f"{key_prefix}/{file_name}.pdf"
        else:
            upload_key = f"{file_name}.pdf"

        upload_to_s3(f"{output_dir}/{file_name}.pdf", upload_bucket, upload_key)
        print('Pdf was uploaded successfully')
    else:
        print('Error when converting to pdf')