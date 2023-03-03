FROM python:3.10.10-slim-buster

WORKDIR /app

COPY requirements.txt /install/requirements.txt

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# Copy our code from the current folder to /app inside the container
COPY . .

CMD ["python", "app.py"]