# FROM python:3-alpine3.13

# LABEL maintainer="https://github.com/AlirezaAnbari"

# ENV PYTHONUNBUFFERED 1

# COPY ./requirements.txt /tmp/requirements.txt
# COPY ./requirements.dev.txt /tmp/requirements.dev.txt
# COPY ./app /app
# WORKDIR /app
# EXPOSE 8000

# ARG DEV=false

# RUN python -m venv /py && \
#     /py/bin/pip install --upgrade pip && \
#     /py/bin/pip install -r /tmp/requirements.txt && \
#     if [ $DEV= "true" ]; \
#         then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
#     fi && \
#     rm -rf /tmp && \
#     adduser \
#         --disabled-password \
#         --no-create-home \
#         django-user

# ENV PATH="py/bin:$PATH"

# USER django-user

FROM python:3-alpine3.13

LABEL maintainer="https://github.com/AlirezaAnbari"

ENV PYTHONUNBUFFERED 1

# Copy requirements files
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt

# Copy the entire app directory
COPY ./app /app

# Set working directory to /app
WORKDIR /app

# Expose port 8000
EXPOSE 8000

# Set ARG and ENV for conditional installation
ARG DEV=false
ENV DEV=${DEV}

# Create a virtual environment
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ "$DEV" = "true" ]; then \
        /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

# Add the virtual environment to the PATH
ENV PATH="/py/bin:$PATH"

# Switch to the django-user
USER django-user
