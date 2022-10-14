# syntax=docker/dockerfile:1.2.1
FROM python:3.8

LABEL name="nabla-hooks" version="2.0.3" \
 description="Image used by our products to build python\
 this image is running on Ubuntu 22.10." \
 com.nabla.vendor="NABLA Incorporated"

RUN apt-get update && \
    apt-get -y install gcc && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Explicitly set user/group IDs
RUN groupadd -r nabla-hooks --gid=999 && useradd -m -d /code -r -g nabla-hooks --uid=999 nabla-hooks

RUN chown -R nabla-hooks:nabla-hooks /code

USER nabla-hooks

WORKDIR /code

RUN pip install --upgrade pip
COPY --chown=nabla-hooks:nabla-hooks ./hooks/requirements-current-3.8.txt /code/requirements.txt

RUN --mount=type=secret,id=pip.conf,dst=/code/.config/pip/pip.conf,uid=999,gid=999 \
python -m pip install --no-cache-dir -r /code/requirements.txt

COPY --chown=nabla-hooks:nabla-hooks . /code/nabla-hooks

WORKDIR /code/nabla-hooks

EXPOSE 80

#CMD ["/home/nabla-hooks/.local/bin/uvicorn", "serve:app", "--host", "0.0.0.0", "--port", "80"]
CMD ["/bin/bash"]

HEALTHCHECK NONE
