FROM python:3-alpine

ENV K8S_VERSION=1.18.2 \
    K8S_ARCH=amd64 \
    FLASK_APP=/api.py \
    FLASK_RUN_HOST=0.0.0.0 \
    FLASK_RUN_PORT=8080 \
    WERKZEUG_RUN_MAIN=true \
    MANIFEST_FILE_PATH=/manifest.json

COPY ./api.py ./manifest.json ./requirements.txt /

RUN pip3 install --upgrade pip && \
    pip3 install -r /requirements.txt && \
    apk add --no-cache curl && \
    curl -LO "https://github.com/kubernetes/kompose/releases/download/v${K8S_VERSION}/kompose-linux-${K8S_ARCH}" -o /usr/bin/kompose &&
    chmod +x /usr/bin/kompose

EXPOSE 8080

CMD ["python3", "-m", "flask", "run"]
