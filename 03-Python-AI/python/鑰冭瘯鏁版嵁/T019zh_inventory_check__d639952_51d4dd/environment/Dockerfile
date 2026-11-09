FROM python:3.13-slim-bookworm

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl jq procps && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /opt/services

COPY resources/requirements.txt /opt/services/requirements.txt
RUN pip install --no-cache-dir -r /opt/services/requirements.txt

COPY resources/mock_services/ /opt/services/mock_services/
COPY resources/inventory/ /opt/services/inventory/

WORKDIR /workspace
COPY resources/fixtures/ /workspace/fixtures/

COPY resources/entrypoint.sh /opt/entrypoint.sh
RUN chmod +x /opt/entrypoint.sh

ENV SERVICES="inventory"
ENV PYTHONPATH="/opt/services"
ENV INVENTORY_FIXTURES="/workspace/fixtures/inventory/products.json"
ENV ERROR_RATE="0"

WORKDIR /app
RUN mkdir -p /app/output /app/scripts /app/intermediate

ENTRYPOINT ["/opt/entrypoint.sh"]
CMD ["bash"]

# --- extra common tools (appended) ---
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl wget git jq procps xz-utils \
    ca-certificates build-essential unzip zip vim && \
    rm -rf /var/lib/apt/lists/*
