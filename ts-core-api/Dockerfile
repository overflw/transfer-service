FROM python:3.10-alpine
ADD . /app
WORKDIR /app

RUN apk add --no-cache --virtual .build-deps gcc build-base \
    && pip install -U setuptools cython \
    && pip install --no-cache-dir --upgrade -r requirements.txt \
    && apk del .build-deps gcc build-base
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8007"]