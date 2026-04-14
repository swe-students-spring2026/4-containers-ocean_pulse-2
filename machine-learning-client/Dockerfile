FROM python:3.12.10
WORKDIR /app

RUN pip install --no-cache-dir pipenv
COPY Pipfile Pipfile.lock /app/
RUN pipenv install --deploy --system --clear
RUN pip cache purge

RUN apt-get update && apt-get install -y libgl1

COPY . /app

CMD ["python", "core/core.py"]
