# service/Dockerfile
FROM python:3.9

# For MacOS
# FROM --platform=linux/amd64  python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

# used to wait for backend and frontend to be available before running test
CMD ["python", "unit_test.py"]
