FROM python:2.7

ENV APPDIR /usr/src/app/
ENV CLAY_CONFIG=config/base.yaml

RUN mkdir -p ${APPDIR}
WORKDIR ${APPDIR}

COPY requirements.txt \
    Makefile \
    setup.py \
    ${APPDIR}

COPY config ${APPDIR}/config/
COPY bootcamp ${APPDIR}/bootcamp/

RUN virtualenv env
RUN . env/bin/activate

RUN pip install -U 'pip>=9'
RUN pip install --no-cache-dir -r requirements.txt
RUN python setup.py install

CMD . env/bin/activate && bootcamp-web

EXPOSE 18888
