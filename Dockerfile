# syntax=docker/dockerfile:1
FROM python:3.11.3-slim

ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt-get update
RUN apt-get install -y chromium xvfb git 

# Tweak below to disable caching
RUN echo 1234

# Clone repo and install requirements
WORKDIR /opt/SassBot
COPY . .
RUN pip3 install -r requirements.txt
    
# ENTRYPOINT ["/usr/bin/python3", "-O", "run.py"]
# ENTRYPOINT ["/usr/bin/python3", "-u", "run.py"]
#CMD ["/bin/sh", "-c", "/usr/bin/python3 -u run.py 2>&1"]
ENTRYPOINT ["/bin/sh", "-c", "./docker-entrypoint.sh"]