FROM python:3.6-alpine3.7

LABEL maintainer="Dmitry Davidov <dmitrii.davidov@gmail.com>"


ADD ./requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

WORKDIR /workspace
ADD ./src ./src
RUN ls

CMD python ./src/main.py
