FROM python:3.13.12

WORKDIR /app

# COPY . . 
ADD . /app

RUN pip install flask

EXPOSE 5001 
#port 5000 not working on my computer

CMD ["python", "app.py"]