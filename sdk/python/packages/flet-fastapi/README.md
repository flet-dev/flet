# Flet for Fast API

## Example

TBD

## Running in production

```
gunicorn -k uvicorn.workers.UvicornWorker your_app:app
```

## Variables

FLET_SECRET_KEY
FLET_SESSION_TIMEOUT - seconds, defaulting to 3,600 seconds.
FLET_OAUTH_STATE_TIMEOUT - seconds, defaulting to 600 seconds.
FLET_MAX_UPLOAD_SIZE - max allowed size of an uploaded file, bytes.