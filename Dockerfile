FROM python:3.5.1

ENV PYTHONPATH /usr/src/app:$PYTHONPATH

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/app

CMD [ "./bin/stretchd.py" ]
