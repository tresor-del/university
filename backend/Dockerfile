FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y python3-dev default-libmysqlclient-dev build-essential

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]