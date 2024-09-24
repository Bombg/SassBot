# syntax=docker/dockerfile:1
FROM python:3.11.3-slim

ENV DEBIAN_FRONTEND=noninteractive
ARG GITHUB_REPO="Bombg/SassBot"
ARG GITHUB_BRANCH="flexiefae"

RUN apt-get update && apt-get dist-upgrade -y

# Install Google Chrome and dependencies
RUN apt-get install -y wget gnupg2
RUN apt-get update
RUN apt-get install -y chromium xvfb python3-pip git libgconf-2-4 unzip htop

# Tweak below to disable caching
RUN echo 1234

# Clone repo and install requirements
RUN cd /opt && \
    git clone https://github.com/${GITHUB_REPO}.git && \
    cd /opt/SassBot && \
    git checkout ${GITHUB_BRANCH} && \
    pip3 install -r requirements.txt

WORKDIR /opt/SassBot
# ENTRYPOINT ["/usr/bin/python3", "-O", "run.py"]
# ENTRYPOINT ["/usr/bin/python3", "-u", "run.py"]
CMD ["/bin/bash", "-c", "/usr/bin/python3 -u run.py 2>&1"]