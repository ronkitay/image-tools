ARG RELEASE
ARG DOCKER_REPO
FROM ${DOCKER_REPO}/python-3-env:${RELEASE}

RUN apt update && apt install -y ffmpeg 

RUN virtualenv /root/.venv

RUN . /root/.venv/bin/activate && pip install exifread ffmpeg-python python-dateutil pillow_heif

RUN echo 'source /root/.venv/bin/activate' >> ${ZSHRC_FILE}

RUN mkdir /root/tools/

ADD tools/rename_by_metadata.py /root/tools/rename_by_metadata.py
ADD tools/rename_by_pattern.py /root/tools/rename_by_pattern.py
ADD tools/remove_numeric_suffix.py /root/tools/remove_numeric_suffix.py

RUN echo 'export PATH=/root/tools/:${PATH}' >> ${ZSHRC_FILE}

WORKDIR /root/proj/
