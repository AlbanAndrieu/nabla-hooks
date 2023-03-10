# syntax=docker/dockerfile:1.2.1

# dockerfile_lint - ignore
# hadolint ignore=DL3007
FROM pytorch/pytorch:1.13.1-cuda11.6-cudnn8-runtime as prebuild
# FROM pytorch/pytorch:1.13.0-cuda11.6-cudnn8-runtime as prebuild
# FROM pytorch/pytorch:1.7.1-cuda11.0-cudnn8-runtime as prebuild
# FROM python:3.10

LABEL name="jm-python" version="2.0.3" \
 description="Image used by our products to build python\
 this image is running on Ubuntu 22.10." \
 com.nabla.vendor="NABLA Incorporated"

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# No interactive frontend during docker build
ENV DEBIAN_FRONTEND=noninteractive \
    DEBCONF_NONINTERACTIVE_SEEN=true

    ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8
ENV TERM="xterm-256color"

# Enable retry logic for apt up to 10 times
# Configure apt to always assume Y
RUN echo "APT::Acquire::Retries \"10\";" > /etc/apt/apt.conf.d/80-retries \
&& echo "APT::Get::Assume-Yes \"true\";" > /etc/apt/apt.conf.d/90assumeyes

# build-essential has gcc
# hadolint ignore=DL3008
RUN apt-get update && \
    apt-get -y install --no-install-recommends build-essential git locales tzdata && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# because of tzdata and the need of noninteractive
ENV TZ "Europe/Paris"
RUN echo "${TZ}" > /etc/timezone
RUN ln -fs /usr/share/zoneinfo/${TZ} /etc/localtime && locale-gen en_US.UTF-8 \
    && dpkg-reconfigure --frontend noninteractive tzdata

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=off

# Explicitly set user/group IDs
RUN groupadd -r jm-python --gid=999 && useradd -m -d /code -r -g jm-python --uid=999 jm-python

RUN chown -R jm-python:jm-python /code

WORKDIR /code

USER jm-python

# RUN --mount=type=secret,id=Pipfile,dst=/code/Pipfile,uid=999,gid=999
COPY --chown=jm-python:jm-python ./hooks/requirements-current-3.8.txt /code/requirements.txt
COPY --chown=jm-python:jm-python Pipfile* /code/

# hadolint ignore=DL3013
# RUN --mount=type=secret,id=pip.conf,dst=/code/.config/pip/pip.conf,uid=999,gid=999 \
RUN --mount=type=secret,id=Pipfile,dst=/code/Pipfile,uid=999,gid=999 \
python -m pip install --upgrade pip && \
python -m pip install --no-cache-dir --user --upgrade pipenv && \
python -m pip install --no-cache-dir --user --upgrade virtualenv && \
python -m pipenv install --site-packages --system
# python -m pip install --no-cache-dir -r /code/requirements.txt

# hadolint ignore=DL3013
# RUN conda install -c conda-forge pipenv
# RUN pipenv install --python /opt/conda/bin/python --site-packages --system
# RUN rm -f Pipfile*

# dockerfile_lint - ignore
# hadolint ignore=DL3007
# FROM prebuild as runtime

USER jm-python

COPY --chown=jm-python:jm-python hooks/ /code/jm-python/hooks/
COPY --chown=jm-python:jm-python serve.py /code/jm-python/
RUN mkdir -p /code/jm-python/var/

ENV PATH=/code/.local/bin/:${PATH}

WORKDIR /code/jm-python

# HEALTHCHECK NONE
HEALTHCHECK CMD curl --fail http://localhost:8080/ping || exit 1

EXPOSE 8080

CMD ["/code/.local/bin/uvicorn", "serve:app", "--host", "0.0.0.0", "--port", "8080"]
# CMD ["/bin/bash"]
