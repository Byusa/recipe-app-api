FROM python:3.9-alpine3.13
LABEL maintainer="byusaapp.com"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
WORKDIR /app  
EXPOSE 8000

ARG DEV=false
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    # alpine to connect to postgresql
    apk add --update --no-cache postgresql-client && \
    # sets virtual dependency package
    apk add --update --no-cache --virtual .tmp-build-deps \
        # listed packages need to install postgres adaptor (postgresql-dev musl-dev )
        build-base postgresql-dev musl-dev && \
    # install it in requirements.txt
    /py/bin/pip install -r /tmp/requirements.txt && \
    # if dev is true install the dev requirements (dependencies)
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    # remove the packages installed to make docker lighweight
    apk del .tmp-build-deps && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

# update the environment
ENV PATH="/py/bin:$PATH"
# don't give it the full root priviledge
USER django-user
