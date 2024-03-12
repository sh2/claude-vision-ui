#!/bin/bash

YYYYMMDD=$(date +%Y%m%d)

podman build --tag claude-vision-ui:${YYYYMMDD} .
