'''
references
subprocess
https://docs.python.org/3/library/subprocess.html
https://www.datacamp.com/tutorial/python-subprocess

libreoffice
https://www.systutorials.com/docs/linux/man/1-soffice/
'''

import os
from io import BytesIO
import tarfile
import boto3
import subprocess
import brotli

libre_office_install_dir = '/tmp/libreoffice'
upload_bucket = 'pdf-bucket'

'''
This function extracts the libreoffice package layer from /opt to 
/tmp directory.

Layers are downloaded into the /opt directory. The allowed size of all unzipped 
files (function + layers) is 250 MB. 
lo.tar.br is downloaded into the /opt directory.  The size of lo.tar.br 
is 96Mb. Therefore, we meet the unzipped file quota. 

The allowed size of content in the /tmp directory is 512 MB to 10,240 MB.
We extract the lo.tar.br into /tmp. The size of the extraction is 370 MB.

soffice.bin path: /tmp/libreoffice/program/soffice.bin
'''
def load_libre_office():
    if os.path.exists(libre_office_install_dir) and os.path.isdir(libre_office_install_dir):
        print('LibreOffice Exists, skipping extraction')
    else:
        print('LibreOffice does not exist, extracting to /tmp')
        buffer = BytesIO()
        with open('/opt/lo.tar.br', 'rb') as brotli_file:
            d = brotli.Decompressor()
            while True:
                chunk = brotli_file.read(1024)
                buffer.write(d.decompress(chunk))
                if len(chunk) < 1024:
                    break

        buffer.seek(0)

        with tarfile.open(fileobj=buffer) as tar:
            tar.extractall('/tmp')
        print('LibreOffice extracted')
    return f'{libre_office_install_dir}/program/soffice.bin'
    
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
def convert_word_to_pdf(soffice_path, word_file_path, output_dir):
    conv_cmd = f"{soffice_path} --headless --norestore --invisible --nodefault --nofirststartwizard --nolockcheck --nologo --convert-to pdf:writer_pdf_Export --outdir {output_dir} {word_file_path}"
    response = subprocess.run(conv_cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if response.returncode != 0:
        return False
    return True

def lambda_handler(event, context):
    #bucket = bucket name that triggered the event
    bucket = event['Records'][0]['s3']['bucket']['name']
    #key: test.docx
    key = event['Records'][0]['s3']['object']['key']

    #key_prefix: ''
    #base_name: test.docx
    key_prefix, base_name = os.path.split(key)
    #download_path = s3 object download path
    download_path = f"/tmp/{base_name}"
    #output_dir = pdf file output path
    output_dir = "/tmp"
    file_name, ext = os.path.splitext(base_name)
    
    download_from_s3(bucket, key, download_path)
    soffice_path = load_libre_office()

    is_converted = convert_word_to_pdf(soffice_path, download_path, output_dir)
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