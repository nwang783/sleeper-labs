FROM node:22-bookworm-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PI_CODING_AGENT_DIR=/tmp/pi

RUN apt-get update \
    && apt-get install -y --no-install-recommends python3 python3-pip ca-certificates git \
    && rm -rf /var/lib/apt/lists/* \
    && npm install -g --ignore-scripts @earendil-works/pi-coding-agent

WORKDIR /benchmark
COPY requirements.txt .
RUN pip3 install --break-system-packages -r requirements.txt
COPY app app
COPY tasks tasks
COPY agent agent
COPY probes probes
COPY scorer.py scorer.py
ENTRYPOINT ["python3", "agent/entrypoint.py"]
