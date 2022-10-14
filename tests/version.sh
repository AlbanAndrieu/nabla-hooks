#!/bin/bash

if [ -z "${PUBLIC_VERSION}" ]; then
  export PUBLIC_VERSION=1.0.0
fi

echo "${PUBLIC_VERSION}"
