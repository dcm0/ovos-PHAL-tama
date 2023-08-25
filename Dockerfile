ARG TAG=alpha
FROM smartgic/ovos-sound-base:${TAG}

ARG BUILD_DATE=unknown
ARG VERSION=unknown

LABEL org.opencontainers.image.title="Open Voice OS OCI TAMA image"
LABEL org.opencontainers.image.description="PHAL is our Platform/Hardware Abstraction Layer, it completely replaces the concept of hardcoded enclosure from mycroft-core-tama"
LABEL org.opencontainers.image.version=${VERSION}
LABEL org.opencontainers.image.created=${BUILD_DATE}
LABEL org.opencontainers.image.vendor="SU"

ARG ALPHA=false
ARG USER=ovos

USER root

COPY --chmod=0755 files/entrypoint.sh /usr/local/bin/entrypoint.sh
COPY . /tmp/ovos_PHAL_tama


RUN pip3 install /tmp/ovos_PHAL_tama


SHELL ["/bin/bash", "-c"]

RUN apt-get update \
    && apt-get install -y libasound2-dev procps ddcutil build-essential python3-dev \
    && if [ "${ALPHA}" == "true" ]; then \
    pip3 install -r /tmp/ovos_PHAL_tama/requirements.txt --pre; \
    else \
    pip3 install -r /tmp/ovos_PHAL_tama/requirements.txt; \
    fi \
	&& pip3 install /tmp/ovos_PHAL_tama \
    && chown ${USER}:${USER} -R /home/${USER} \
    && apt-get --purge remove --purge -y libasound2-dev build-essential python3-dev \
    && apt-get --purge autoremove -y \
    && apt-get clean \
    && rm -rf ${HOME}/.cache /var/lib/apt /var/log/{apt,dpkg.log} /tmp/ovos_PHAL_tama

USER $USER

ENTRYPOINT ["/bin/bash", "/usr/local/bin/entrypoint.sh"]

WORKDIR /home/${USER}