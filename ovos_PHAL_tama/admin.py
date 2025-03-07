from ovos_plugin_manager.phal import find_admin_plugins
from ovos_utils import wait_for_exit_signal
from ovos_config import Configuration
from ovos_utils.log import LOG, init_service_logger

from ovos_PHAL_tama import PHAL


def on_admin_ready():
    LOG.info('PHAL Tama Admin is ready.')


def on_admin_stopping():
    LOG.info('PHAL Tama Admin is shutting down...')


def on_admin_error(e='Unknown'):
    LOG.error(f'PHAL Tama Admin failed to launch ({e}).')


def on_admin_alive():
    LOG.info('PHAL Tama Admin is alive')


def on_admin_started():
    LOG.info('PHAL Tama Admin is started')


class AdminPHAL(PHAL):
    """
    Args:
        config (dict): PHAL admin config, usually from mycroft.conf PHAL.admin section
        bus (MessageBusClient): mycroft messagebus connection
        watchdog: (callable) function to call periodically indicating
                  operational status.
    """

    def __init__(self, config=None, bus=None, on_ready=on_admin_ready, on_error=on_admin_error,
                 on_stopping=on_admin_stopping, on_started=on_admin_started, on_alive=on_admin_alive,
                 watchdog=lambda: None, name="PHAL.tama.admin", **kwargs):
        if not config:
            try:
                config = Configuration()
                config = config.get("TAMA", {}).get("admin", {})
            except:
                config = {}
        super().__init__(config, bus, on_ready, on_error, on_stopping, on_started, on_alive, watchdog, name, **kwargs)

    def load_plugins(self):
        for name, plug in find_admin_plugins().items():
            config = self.config.get(name) or {}
            enabled = config.get("enabled")
            if not enabled:
                continue  # require explicit enabling by user
            if hasattr(plug, "validator"):
                enabled = plug.validator.validate(config)

            if enabled:
                try:
                    self.drivers[name] = plug(bus=self.bus, config=config)
                    LOG.info(f"PHAL Tama Admin plugin loaded: {name}")
                except Exception:
                    LOG.exception(f"failed to load PHAL Tama Admin plugin: {name}")
                    continue


def main(ready_hook=on_admin_ready, error_hook=on_admin_error, stopping_hook=on_admin_stopping):
    # config read from mycroft.conf
    # "PHAL": {
    #   "admin": {
    #     "ovos-PHAL-plugin-system": {"enabled": True}
    #   }
    # }
    init_service_logger("PHAL_tama_admin")
    phal = AdminPHAL(on_error=error_hook, on_ready=ready_hook, on_stopping=stopping_hook)
    phal.start()
    wait_for_exit_signal()
    phal.shutdown()


if __name__ == "__main__":
    main()
