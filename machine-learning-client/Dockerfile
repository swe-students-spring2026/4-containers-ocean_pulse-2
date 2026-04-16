FROM python:3.12.10

WORKDIR /app

RUN pip install --no-cache-dir pipenv

COPY . /app

RUN pipenv install --deploy --system --clear

RUN apt-get update && apt-get install -y libgl1

CMD ["python3", "-u", "core/core.py"]