# syntax=docker/dockerfile:1
FROM python:3.11.3-slim

ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt update -y
RUN apt install -y chromium xvfb git

# Tweak below to disable caching
RUN echo 1234

# Clone repo and install requirements
WORKDIR /opt/SassBot
COPY . .
RUN pip3 install -r requirements.txt

# Uncomment the below block if you have a slow machine and need a version of nodriver that waits longer for the browser
# https://github.com/Bombg/nodriver has a longer wait built in. (hopefully official version will add it as an option later)
# Clone the above and create a copy of it in your sassbot directory 'cp -r path/to/nodriver/repo ./nodriver'
RUN pip3 install git+https://github.com/Bombg/nodriver.git

RUN chmod +x docker-entrypoint.sh
    
#CMD ["/bin/sh", "-c", "/usr/bin/python3 -u run.py 2>&1"]
ENTRYPOINT ["/bin/sh", "-c", "./docker-entrypoint.sh"]