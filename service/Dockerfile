# service/Dockerfile
FROM python:3.9

# For MacOS
# FROM --platform=linux/amd64  python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

EXPOSE 8080
CMD ["python", "app.py"]
