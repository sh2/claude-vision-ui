#!/bin/bash

export ANTHROPIC_API_KEY=
export ANTHROPIC_PROXY=

streamlit run src/vision-ui.py \
    --browser.gatherUsageStats=false \
    --server.maxUploadSize 20
