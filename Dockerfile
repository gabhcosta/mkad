FROM python:3.8

WORKDIR /app

COPY . .

RUN pip install -e .

ENTRYPOINT ["python", "-u", "./mkad/main.py"]