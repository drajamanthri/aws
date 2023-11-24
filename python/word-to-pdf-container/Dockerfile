FROM public.ecr.aws/lambda/python:latest-x86_64

#if a command needs to run in a specific folder, the same RUN should cd into the foler
# ex RUN cd /tmp \
#    && ls


#install supporting packages for installing and running libreoffice
#lambda base images use dnf instead of yum
RUN dnf -y update \
    && dnf clean all \
    && dnf -y install wget java tar gzip libXinerama cairo cups

#download libreoffice and unpack libreoffice
RUN cd /tmp \
    && wget https://download.documentfoundation.org/libreoffice/stable/7.6.3/rpm/x86_64/LibreOffice_7.6.3_Linux_x86-64_rpm.tar.gz \
    && tar xvf LibreOffice_7.6.3_Linux_x86-64_rpm.tar.gz
    
#show extracted package
RUN cd /tmp \
    && ls
    
#install libreoffice
# dnf -y install *.rpm didn't work. It seems like dnf can not install local rpms
RUN cd /tmp/LibreOffice_7.6.3.2_Linux_x86-64_rpm/RPMS/ \
    && rpm -Uvh *.rpm
    
#clean up
RUN cd /tmp
RUN rm -rf LibreOffice_7.6.3.2_Linux_x86-64_rpm 
RUN rm -rf LibreOffice_7.6.3_Linux_x86-64_rpm.tar.gz 

# Copy requirements.txt
COPY requirements.txt ${LAMBDA_TASK_ROOT}

# Install the specified packages
RUN pip install -r requirements.txt

# Copy function code
COPY lambda_function.py ${LAMBDA_TASK_ROOT}

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "lambda_function.handler" ]

#HOME is where libreoffice7.6 is run by the python script. 
#lambda has permission to /tmp
ENV HOME=/tmp

#Test libreoffice
# RUN echo "test libreoffice"

# RUN touch /tmp/test.txt \
#     && libreoffice7.6 --headless --invisible --nodefault --view \
#         --nolockcheck --nologo --norestore --convert-to pdf \
#         --outdir /tmp /tmp/test.txt \
#     && ls /tmp