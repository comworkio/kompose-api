FROM python:3-alpine

ENV ENABLE_KUBECTL_APPLY=false \
    K8S_VERSION=1.18.2 \
    KOMPOSE_VERSION_N=1.22.0 \
    KOMPOSE_VERSION_NLESS1=1.21.0 \
    ARCH=amd64 \
    FLASK_APP=/api.py \
    FLASK_RUN_HOST=0.0.0.0 \
    FLASK_RUN_PORT=8080 \
    WERKZEUG_RUN_MAIN=true \
    MANIFEST_FILE_PATH=/manifest.json

COPY ./api.py ./manifest.json ./versions.sh ./konvert.sh ./requirements.txt /

RUN pip3 install --upgrade pip && \
    pip3 install -r /requirements.txt && \
    apk add --no-cache curl bash jq && \
    curl -L "https://storage.googleapis.com/kubernetes-release/release/v${K8S_VERSION}/bin/linux/${ARCH}/kubectl" -o /usr/bin/kubectl && \
    chmod +x /usr/bin/kubectl /versions.sh /konvert.sh && \
    curl -L "https://github.com/kubernetes/kompose/releases/download/v${KOMPOSE_VERSION_N}/kompose-linux-${ARCH}" -o /usr/bin/kompose-${KOMPOSE_VERSION_N} && \
    chmod +x /usr/bin/kompose-${KOMPOSE_VERSION_N} && \
    curl -L "https://github.com/kubernetes/kompose/releases/download/v${KOMPOSE_VERSION_NLESS1}/kompose-linux-${ARCH}" -o /usr/bin/kompose-${KOMPOSE_VERSION_NLESS1} && \
    chmod +x /usr/bin/kompose-${KOMPOSE_VERSION_NLESS1}

EXPOSE 8080

CMD ["python3", "-m", "flask", "run"]
