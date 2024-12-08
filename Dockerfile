FROM python:3.12-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /usr/src/app
COPY src/requirements.txt src/run.sh src/vision-ui.py ./
RUN pip install --no-cache-dir --requirement requirements.txt
CMD ["./run.sh"]
