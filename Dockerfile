FROM python:3.9.7-alpine

RUN apk add build-base

COPY requirements.txt ./

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "main:app", "-root-path", "network"]
