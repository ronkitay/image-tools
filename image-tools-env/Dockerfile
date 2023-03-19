ARG RELEASE
FROM ronkitay/python-3.9-env:${RELEASE}

# Image metadata retrival
RUN pip install exifread

# Video metadata retrival
RUN apt update && apt install -y ffmpeg
RUN pip install ffmpeg-python
RUN pip install python-dateutil

RUN mkdir /root/tools/

ADD tools/rename_by_metadata.py /root/tools/rename_by_metadata.py
ADD tools/rename_by_pattern.py /root/tools/rename_by_pattern.py
ADD tools/remove_numeric_suffix.py /root/tools/remove_numeric_suffix.py

RUN echo 'export PATH=/root/tools/:${PATH}' >> ${ZSHRC_FILE}
