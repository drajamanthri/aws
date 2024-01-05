#FROM public.ecr.aws/lambda/python:latest-x86_64
FROM public.ecr.aws/lambda/python:3.11

COPY app.py requirements.txt ./

RUN python3.11 -m pip install -r requirements.txt -t .

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambda_handler"]

#libreoffice setup
#if a command needs to run in a specific folder, the same RUN should cd into the foler
# ex RUN cd /tmp \
#    && ls

#install supporting packages for installing and running libreoffice
#New lambda base images use dnf instead of yum
RUN yum -y update \
    && yum clean all \
    && yum -y install wget java tar gzip libXinerama cairo cups

#download libreoffice and unpack libreoffice
#make sure the package exists. If it does not exist, use a diffirent package. 
#if the package is different, update the extracted file names accordingly.
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