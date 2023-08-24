FROM ghcr.io/openvoiceos/core:dev

COPY . /tmp/ovos-phal-tama
RUN pip3 install /tmp/ovos-phal-tama

USER mycroft

ENTRYPOINT ovos_PHAL_tama