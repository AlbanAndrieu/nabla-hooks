# syntax=docker/dockerfile:1.15

# dockerfile_lint - ignore
# hadolint ignore=DL3007
FROM pytorch/pytorch:1.13.1-cuda11.6-cudnn8-runtime AS prebuild
# FROM pytorch/pytorch:1.13.0-cuda11.6-cudnn8-runtime AS prebuild
# FROM pytorch/pytorch:1.7.1-cuda11.0-cudnn8-runtime AS prebuild
# FROM python:3.10

# dockerfile_lint - ignore
LABEL name="nabla-hooks" version="1.0.6" \
 description="Image used by our products to build python\
 this image is running on Ubuntu 22.10." \
 com.nabla.vendor="NABLA Incorporated"

# dockerfile_lint - ignore
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# No interactive frontend during docker build
# dockerfile_lint - ignore
ENV DEBIAN_FRONTEND=noninteractive
ENV DEBCONF_NONINTERACTIVE_SEEN=true

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
# python
ENV PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    # poetry
    # https://python-poetry.org/docs/configuration/#using-environment-variables
    POETRY_VERSION=1.8.3 \
    # make poetry install to this location
    POETRY_HOME="/opt/poetry" \
    POETRY_NO_INTERACTION=1 \
    # make poetry create the virtual environment in the project's root
    # it gets named `.venv`
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    # do not ask any interactive question
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache \
    # paths
    # this is where our requirements + virtual environment will live
    # PYSETUP_PATH="/opt/pysetup" \
    PYSETUP_PATH="/code" \
    VENV_PATH="/code/.venv"

# prepend poetry and venv to path
ENV PATH="${POETRY_HOME}/bin:$VENV_PATH/bin:$PATH"

# Explicitly set user/group IDs
RUN groupadd -r jm-python --gid=999 && useradd -m -d /code -r -g jm-python --uid=999 jm-python

RUN chown -R jm-python:jm-python /code

WORKDIR /code

USER jm-python

# RUN --mount=type=secret,id=Pipfile,dst=/code/Pipfile,uid=999,gid=999
COPY --chown=jm-python:jm-python --chmod=755 ./hooks/requirements-current-3.8.txt /code/requirements.txt
COPY --chown=jm-python:jm-python --chmod=755 Pipfile* /code/

# RUN --mount=type=secret,id=pip.conf,dst=/code/.config/pip/pip.conf,uid=999,gid=999 \
# hadolint ignore=DL3013,DL3042
RUN --mount=type=secret,id=Pipfile,dst=/code/Pipfile,uid=999,gid=999 \
python -m pip install --no-cache-dir --upgrade pip==25.1.1 && \
python -m pip install --no-cache-dir poetry=="${POETRY_VERSION}" ansible==11.5.0 && \
python -m pip install --no-cache-dir --user --upgrade pipenv==2023.7.23 && \
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

COPY --chown=jm-python:jm-python --chmod=755 hooks/ /code/jm-python/hooks/
COPY --chown=jm-python:jm-python --chmod=755 nabla/ /code/jm-python/nabla/
COPY --chown=jm-python:jm-python --chmod=755 serve.py /code/jm-python/
RUN mkdir -p /code/jm-python/var/

ENV PATH=/code/.local/bin/:${PATH}

WORKDIR /code/jm-python

# HEALTHCHECK NONE
HEALTHCHECK CMD curl --fail http://localhost:8080/v1/ping || exit 1

EXPOSE 8080

CMD ["/code/.local/bin/uvicorn", "serve:app", "--host", "0.0.0.0", "--port", "8080"]
# CMD ["/bin/bash"]
