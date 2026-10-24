# syntax=docker/dockerfile:1

# dockerfile_lint - ignore
FROM python:3.14-slim-bookworm AS prebuild

# dockerfile_lint - ignore
LABEL name="nabla-hooks" version="1.0.7" \
 description="Image used by our products to build python\
 this image is running on Debian bookworm." \
 com.nabla.vendor="NABLA Incorporated"

# dockerfile_lint - ignore
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# No interactive frontend during docker build
# dockerfile_lint - ignore
ENV DEBIAN_FRONTEND=noninteractive
ENV DEBCONF_NONINTERACTIVE_SEEN=true

ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US:en
ENV LC_ALL=en_US.UTF-8
ENV TERM="xterm-256color"

# Enable retry logic for apt up to 10 times
# Configure apt to always assume Y
RUN echo "APT::Acquire::Retries \"10\";" > /etc/apt/apt.conf.d/80-retries \
&& echo "APT::Get::Assume-Yes \"true\";" > /etc/apt/apt.conf.d/90assumeyes

# curl is needed by the HEALTHCHECK
# hadolint ignore=DL3008
RUN apt-get update && \
    apt-get -y install --no-install-recommends curl git locales tzdata && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# because of tzdata and the need of noninteractive
ENV TZ="Europe/Paris"
RUN echo "${TZ}" > /etc/timezone
RUN ln -fs /usr/share/zoneinfo/${TZ} /etc/localtime \
    && sed -i 's/^# *\(en_US.UTF-8\)/\1/' /etc/locale.gen && locale-gen \
    && dpkg-reconfigure --frontend noninteractive tzdata

# uv : https://docs.astral.sh/uv/guides/integration/docker/
COPY --from=ghcr.io/astral-sh/uv:0.13.5 /uv /uvx /bin/

# Turns off buffering for easier container logging
# python
ENV PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    # uv
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never \
    UV_PROJECT_ENVIRONMENT="/code/.venv" \
    # paths
    VENV_PATH="/code/.venv"

# prepend venv to path
ENV PATH="$VENV_PATH/bin:$PATH"

# Explicitly set user/group IDs
RUN groupadd -r jm-python --gid=999 && useradd -m -d /code -r -g jm-python --uid=999 jm-python

RUN mkdir -p /code/jm-python && chown -R jm-python:jm-python /code

WORKDIR /code/jm-python

USER jm-python

# Install dependencies first (cached layer), then the project
RUN --mount=type=cache,target=/code/.cache/uv,uid=999,gid=999 \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-default-groups --group api

COPY --chown=jm-python:jm-python --chmod=755 pyproject.toml uv.lock README.md LICENSE /code/jm-python/
COPY --chown=jm-python:jm-python --chmod=755 bin/ /code/jm-python/bin/
COPY --chown=jm-python:jm-python --chmod=755 hooks/ /code/jm-python/hooks/
COPY --chown=jm-python:jm-python --chmod=755 nabla/ /code/jm-python/nabla/
COPY --chown=jm-python:jm-python --chmod=755 serve.py /code/jm-python/

RUN --mount=type=cache,target=/code/.cache/uv,uid=999,gid=999 \
    uv sync --locked --no-editable --no-default-groups --group api

RUN mkdir -p /code/jm-python/var/

# HEALTHCHECK NONE
HEALTHCHECK CMD curl --fail http://localhost:8080/v1/ping || exit 1

EXPOSE 8080

CMD ["uvicorn", "serve:app", "--host", "0.0.0.0", "--port", "8080"]
# CMD ["/bin/bash"]
