ARG RELEASE
FROM ronkitay/python-3.9-env:${RELEASE}

# Image metadata retrival
RUN pip install exifread

# Video metadata retrival
RUN apt update && apt install -y ffmpeg
RUN pip install ffmpeg-python

RUN mkdir /root/image-tools/

ADD tools/rename_by_metadata.py /root/image-tools/rename_by_metadata.py

RUN echo 'export PATH=/root/image-tools:${PATH}' >> ${ZSHRC_FILE}
