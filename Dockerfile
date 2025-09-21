FROM python:3.13-slim AS base 

WORKDIR /pyrade

COPY ./requirements.txt ./requirements.txt

COPY --chown=1001:0 ./ ./

#USER 1001

RUN pip install -r requirements.txt

ENV DOCKER=true

ENTRYPOINT [ "python3", "rade.py" ]