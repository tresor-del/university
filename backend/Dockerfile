FROM python:3.13-slim

WORKDIR /app

# ligne a supprimer si vous ne télechargé pas les packages en local et de les installer en mode hors ligne sur docker
COPY packages/ /tmp/packages/

COPY requirements.txt .

RUN pip install --no-index --find-links=/tmp/packages/ -r requirements.txt 
# et dans ce cas, faites RUN pip install --no-cache-dir -r requirements.txt plutôt


COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]