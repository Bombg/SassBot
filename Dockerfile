# Build Stage
FROM python:3.11.3-slim AS build

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update -y && apt install -y git

RUN python3 -m venv /venv
ENV PATH=/venv/bin:$PATH

COPY requirements.txt .
RUN pip install -r requirements.txt && \
    pip install uvloop

# Buidling final image, moving over venv
FROM python:3.11.3-slim

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /opt/SassBot

RUN apt update -y && apt install -y --no-install-recommends chromium xvfb

COPY --from=build /venv /venv
ENV PATH=/venv/bin:$PATH

COPY . .

RUN chmod +x docker-entrypoint.sh
    
ENTRYPOINT ["/bin/sh", "-c", "./docker-entrypoint.sh"]