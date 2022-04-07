FROM python:3.8
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install python-multipart
COPY ./app ./app

CMD ["python", "./app/main.py"]
