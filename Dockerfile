# syntax=docker/dockerfile:1
FROM ubuntu:jammy

ENV DEBIAN_FRONTEND=noninteractive
ARG GITHUB_REPO="Bombg/SassBot"
ARG GITHUB_BRANCH="flexiefae"

RUN apt-get update
RUN apt-get dist-upgrade -y

# Install Google Chrome and dependencies
RUN apt-get install -y wget gnupg2
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list
RUN apt-get update
RUN apt-get install -y python3.10 python3-pip google-chrome-stable git libgconf-2-4 unzip htop

# Tweak below to disable caching
RUN echo 1234

# Install chromedriver
RUN mkdir /opt/chromedriver && \
    wget -q --continue -P /opt/chromedriver "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/120.0.6099.109/linux64/chromedriver-linux64.zip" && \
    unzip /opt/chromedriver/chromedriver-linux64.zip -d /opt/chromedriver && \
    mv /opt/chromedriver/chromedriver-linux64/chromedriver /usr/bin/chromedriver

# Tweak below to disable caching
RUN echo 1234

# Clone repo and install requirements
RUN cd /opt && \
    git clone https://github.com/${GITHUB_REPO}.git && \
    cd /opt/SassBot && \
    git checkout ${GITHUB_BRANCH} && \
    pip install -r requirements.txt && \
    pip install uvloop

WORKDIR /opt/SassBot
# ENTRYPOINT ["/usr/bin/python3", "-O", "run.py"]
# ENTRYPOINT ["/usr/bin/python3", "-u", "run.py"]
CMD ["/bin/bash", "-c", "/usr/bin/python3 -u run.py 2>&1"]
