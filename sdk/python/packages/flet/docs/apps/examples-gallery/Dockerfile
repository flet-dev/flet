FROM python:3-alpine

WORKDIR /app

COPY packages/flet/docs/apps/examples-gallery .
COPY examples/controls ./examples/controls

RUN pip install --no-cache-dir .

EXPOSE 8000

CMD ["python", "src/main.py"]
