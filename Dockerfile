FROM python:3.13.12

WORKDIR /app

ADD . /app

RUN pip install flask pymongo

EXPOSE 5000

CMD ["python", "app.py"]
