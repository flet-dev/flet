FROM python:3-alpine

WORKDIR /app

COPY pyproject.toml ./
RUN pip install --no-cache-dir .

COPY . .

EXPOSE 8080

CMD ["python", "./main.py"]
