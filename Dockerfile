FROM ghcr.io/openvoiceos/core:dev

COPY . /tmp/ovos_PHAL_tama
RUN pip3 install /tmp/ovos_PHAL_tama

USER ovos

ENTRYPOINT ovos_PHAL_tama