#!/bin/bash

podman run \
        --detach \
        --restart=always \
        --publish=8501:8501 \
        --env=ANTHROPIC_API_KEY= \
        --env=ANTHROPIC_PROXY= \
        --name=claude-vision-ui \
        claude-vision-ui:20240101
