FROM python:3.12.1-alpine3.19

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

CMD ["sh", "-c", "python3 app/manage.py migrate ; exec python3 app/manage.py runserver 0.0.0.0:$SERVER_PORT"]