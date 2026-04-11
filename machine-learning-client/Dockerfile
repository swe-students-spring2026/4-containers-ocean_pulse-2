FROM python:3.13.12
WORKDIR /app

RUN pip install --no-cache-dir pipenv
COPY Pipfile Pipfile.lock /app/
RUN pipenv install --deploy --system

RUN echo 'export PS1="\[\e[36m\]\u@\h\[\e[0m\]:\[\e[33m\]\w\[\e[0m\]\$ "' >> /root/.bashrc
RUN echo 'alias ll="ls -la"' >> /root/.bashrc