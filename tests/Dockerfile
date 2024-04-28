# ================================== BUILDER ===================================
ARG  PYTHON_VERSION=3.11
FROM python:${PYTHON_VERSION} as build

# Environments to reduce size of docker image
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONFAULTHANDLER=true
ENV PYTHONUNBUFFERED=true
ENV PYTHONHASHSEED=random
ENV PIP_NO_CACHE_DIR=true
ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ENV PIP_DEFAULT_TIMEOUT=100

# Install system updates and tools
RUN apt-get update 
RUN python -m pip install --upgrade pip

# Add workdir and user non root user
WORKDIR /srv
RUN useradd -m sid

# Copy and install testing requirements
COPY --chown=sid:sid . /srv
RUN python -m pip install -r requirements.txt

# Change to non root user and expose port
USER sid

# Define entrypoint and default command
ENTRYPOINT [ "python", "-m", "pytest" ]
CMD [ "-n=auto", "." ]
