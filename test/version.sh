#!/bin/bash

if [ -z "$PUBLIC_VERSION" ]; then
  export PUBLIC_VERSION=1.07.04.000
fi

echo "$PUBLIC_VERSION"
