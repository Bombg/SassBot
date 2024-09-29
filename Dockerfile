# syntax=docker/dockerfile:1
FROM python:3.11.3-slim

ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt update -y
RUN apt install -y chromium xvfb git

WORKDIR /opt/SassBot
COPY . .

# Clone repo and install requirements
RUN pip install -r requirements.txt && \
    pip install uvloop

RUN chmod +x docker-entrypoint.sh
    
ENTRYPOINT ["/bin/sh", "-c", "./docker-entrypoint.sh"]