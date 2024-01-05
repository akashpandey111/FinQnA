FROM apache/airflow:slim-latest-python3.11

WORKDIR /datagen

COPY . .

ADD ./requirements.txt /datagen/requirements.txt
RUN python3 -m pip install -U pip setuptools
RUN python3 -m pip install -r requirements.txt

RUN airflow db init
CMD ["webserver"]
