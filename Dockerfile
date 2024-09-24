# syntax=docker/dockerfile:1
FROM python:3.11.3-slim
ARG GITHUB_REPO="Bombg/SassBot"
ARG GITHUB_BRANCH="flexiefae"

ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt update -y
RUN apt install -y chromium xvfb git

# Tweak below to disable caching
RUN echo 1234

# Clone repo and install requirements
RUN cd /opt && \
    git clone https://github.com/${GITHUB_REPO}.git && \
    cd /opt/SassBot && \
    git checkout ${GITHUB_BRANCH} && \
    pip install -r requirements.txt 

WORKDIR /opt/SassBot
RUN chmod +x docker-entrypoint.sh
    
ENTRYPOINT ["/bin/sh", "-c", "./docker-entrypoint.sh"]