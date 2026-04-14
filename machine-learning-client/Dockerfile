FROM python:3.12.10
WORKDIR /app

RUN pip install --no-cache-dir pipenv
COPY Pipfile Pipfile.lock /app/
RUN pipenv install --deploy --system --clear
RUN pip cache purge

RUN apt-get update && apt-get install -y libgl1
RUN echo 'export PS1="\[\e[36m\]dev@\h\[\e[0m\]:\[\e[33m\]\w\[\e[0m\]\$ "' >> /etc/bash.bashrc
RUN echo 'alias ll="ls -la"' >> /etc/bash.bashrc
