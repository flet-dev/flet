FROM python:3-alpine

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir .

EXPOSE 8000

CMD ["python", "main.py"]
