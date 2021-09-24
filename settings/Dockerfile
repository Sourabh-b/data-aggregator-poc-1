FROM containers.cisco.com/hb_containers_gen/ubuntu:20.04

ARG CONFIG_BASE_PATH="settings"
ARG CONFIG_ENV_PATH=${CONFIG_ENV_PATH}

# Copy bundle to volume container
COPY ${CONFIG_BASE_PATH}/${CONFIG_ENV_PATH} /config