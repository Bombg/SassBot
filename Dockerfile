FROM python:3.11.3-slim AS build

ENV DEBIAN_FRONTEND=noninteractive
# Build dummy packages to skip installing them and their dependencies -- Copied from FlareSolverr
RUN apt update -y && apt install -y git \
    && apt-get install -y --no-install-recommends equivs \
    && equivs-control libgl1-mesa-dri \
    && printf 'Section: misc\nPriority: optional\nStandards-Version: 3.9.2\nPackage: libgl1-mesa-dri\nVersion: 99.0.0\nDescription: Dummy package for libgl1-mesa-dri\n' >> libgl1-mesa-dri \
    && equivs-build libgl1-mesa-dri \
    && mv libgl1-mesa-dri_*.deb /libgl1-mesa-dri.deb \
    && equivs-control adwaita-icon-theme \
    && printf 'Section: misc\nPriority: optional\nStandards-Version: 3.9.2\nPackage: adwaita-icon-theme\nVersion: 99.0.0\nDescription: Dummy package for adwaita-icon-theme\n' >> adwaita-icon-theme \
    && equivs-build adwaita-icon-theme \
    && mv adwaita-icon-theme_*.deb /adwaita-icon-theme.deb

RUN python3 -m venv /venv
ENV PATH=/venv/bin:$PATH

COPY requirements.txt .
RUN pip install -r requirements.txt && \
    pip install uvloop

# Buidling final image, moving over venv
FROM python:3.11.3-slim
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /opt/SassBot

RUN apt update -y && apt install -y --no-install-recommends chromium xvfb \
    # Remove temporary files and hardware decoding libraries -- Copied from FlareSolverr
    && rm -rf /var/lib/apt/lists/* \
    && rm -f /usr/lib/x86_64-linux-gnu/libmfxhw* \
    && rm -f /usr/lib/x86_64-linux-gnu/mfx/* 

COPY --from=build /venv /venv
ENV PATH=/venv/bin:$PATH
COPY . .

RUN chmod +x docker-entrypoint.sh
ENTRYPOINT ["/bin/sh", "-c", "./docker-entrypoint.sh"]