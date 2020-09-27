FROM python:3.8

WORKDIR /usr/src/app

COPY . .

RUN pip install .

RUN python -m playwright install

ENTRYPOINT ["dynalist_backuper"]


