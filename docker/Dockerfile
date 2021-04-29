FROM python:3.8-buster

LABEL maintainer="ricardo.savii@dafiti.com.br"

COPY Pipfile Pipfile.lock ./
RUN pip install --no-cache-dir pipenv==2020.8.13 \
    && apt-get update -y \
    && apt-get install -y --no-install-recommends \
        python3-dev \
        libev-dev \
        nginx \
    && pipenv install --system --ignore-pipfile --deploy --clear \
    && apt-get remove -y gcc python3-dev libssl-dev \
    && apt-get autoremove -y \
    && pip uninstall pipenv -y \
    && rm -rf /var/lib/apt/lists/*

# Set some environment variables. PYTHONUNBUFFERED keeps Python from
# buffering our standard output stream, which means that logs can be
# delivered to the user quickly. PYTHONDONTWRITEBYTECODE keeps Python
# from writing the .pyc files which are unnecessary in this case. We
# also update PATH so that the train and serve programs are found when
# the container is invoked.
ENV PYTHONUNBUFFERED=TRUE
ENV PYTHONDONTWRITEBYTECODE=TRUE
ENV PATH="/opt/program/:${PATH}"
ENV ML_PREFIX="/opt/ml/"
ENV ENVIRON="DOCKER"

# Set up the program and config in the image
COPY src /opt/program

WORKDIR /opt/program
RUN chmod +x /opt/program/train
RUN chmod +x /opt/program/serve

EXPOSE 8080