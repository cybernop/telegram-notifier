FROM python:3.7 AS builder

WORKDIR /notifier

COPY telnotif/ telnotif/
COPY setup.py .

RUN python setup.py sdist bdist_wheel

#######

FROM python:3.7-alpine

WORKDIR /notifier

COPY main.py .

COPY --from=builder /notifier/dist/ dist/

RUN apk add --no-cache --virtual .build-deps \
    build-base \
    libffi-dev \
    libressl-dev \
    && pip install $(ls dist/*.whl) \
    && apk del .build-deps

RUN apk add --no-cache \
    libstdc++


ENTRYPOINT ["python", "main.py"]
