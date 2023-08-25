from ovos_plugin_manager.phal import find_phal_plugins
from ovos_config import Configuration
from ovos_utils.log import LOG
from ovos_bus_client.client import MessageBusClient, Message
from ovos_utils.process_utils import ProcessStatus, StatusCallbackMap
from ovos_workshop import OVOSAbstractApplication


import subprocess
import time
import sys
from alsaaudio import Mixer
from threading import Thread, Timer

import serial
import colorsys
from ovos_PHAL_tama.arduino import EnclosureReader, EnclosureWriter
from ovos_PHAL_tama.arduino import EnclosureArduino
from ovos_PHAL_tama.eyes import EnclosureEyes
from ovos_PHAL_tama.gaze import EnclosureGaze



def on_ready():
    LOG.info('PHAL is ready.')


def on_stopping():
    LOG.info('PHAL is shutting down...')


def on_error(e='Unknown'):
    LOG.error(f'PHAL failed to launch ({e}).')


def on_alive():
    LOG.info('PHAL is alive')


def on_started():
    LOG.info('PHAL is started')


class PHAL(OVOSAbstractApplication):
    """
    Args:
        config (dict): PHAL config, usually from mycroft.conf
        bus (MessageBusClient): mycroft messagebus connection
        watchdog: (callable) function to call periodically indicating
                  operational status.
    """

    def __init__(self, config=None, bus=None,
                 on_ready=on_ready, on_error=on_error,
                 on_stopping=on_stopping, on_started=on_started, on_alive=on_alive,
                 watchdog=lambda: None, skill_id="ovos.PHAL.tama", **kwargs):
        if not bus:
            bus = MessageBusClient()
            bus.run_in_thread()
        super().__init__(skill_id=skill_id, bus=bus)
        ready_hook = kwargs.get('ready_hook', on_ready)
        error_hook = kwargs.get('error_hook', on_error)
        stopping_hook = kwargs.get('stopping_hook', on_stopping)
        alive_hook = kwargs.get('alive_hook', on_alive)
        started_hook = kwargs.get('started_hook', on_started)
        callbacks = StatusCallbackMap(on_ready=ready_hook,
                                      on_error=error_hook,
                                      on_stopping=stopping_hook,
                                      on_alive=alive_hook,
                                      on_started=started_hook)
        self.status = ProcessStatus("PHAL", callback_map=callbacks)
        self._watchdog = watchdog  # TODO implement
        self.config = config or Configuration().get("TAMA") or {
            "port": "/dev/ttyS0",
            "rate": "9600",
            "timeout": 5
        }  # TODO
        self.drivers = {}
        self.__init_serial()
        self.reader = EnclosureReader(self.serial, self.bus)
        self.writer = EnclosureWriter(self.serial, self.bus)
        self.status.bind(self.bus)

        self.bus.on("enclosure.started", self.on_arduino_responded)
        self.eyes = EnclosureEyes(self.bus, self.writer)
        self.system = EnclosureArduino(self.bus, self.writer)
        self.gaze = EnclosureGaze(self.bus, self.writer)
        self.arduino_responded = True
        

    def on_arduino_responded(self, event=None):
        self.eyes = EnclosureEyes(self.bus, self.writer)
        self.system = EnclosureArduino(self.bus, self.writer)
        self.__register_events()
        self.__reset()
        self.arduino_responded = True


    def __init_serial(self):
        try:
            #For TAMA these should be '/dev/ttyS0',9600)#IK0312
            #added to the default config
            self.port = self.config.get("port")
            #self.port = '/dev/ttyS0'
            self.rate = self.config.get("rate")
            #self.rate = 9600
            self.timeout = self.config.get("timeout")
            self.serial = serial.serial_for_url(
                url=self.port, baudrate=self.rate, timeout=self.timeout)
            LOG.info("Connected to: %s rate: %s timeout: %s" %
                     (self.port, self.rate, self.timeout))
        except Exception:
            LOG.error("Impossible to connect to serial port: " +
                      str(self.port))
            raise

    def __register_events(self):
        self.bus.on('enclosure.reset', self.__reset)

    def __reset(self, event=None):
        # Reset both the position and the eye colour to indicate the unit is
        # ready for input.
        self.eyes.reset()

    def speak(self, text):
        self.bus.emit(Message("speak", {'utterance': text}))

    def check_for_response(self):
        if not self.arduino_responded:
            # There is nothing on the other end of the serial port
            # close these serial-port readers and this process
            self.writer.stop()
            self.serial.close()
            self.bus.close()

    def stop(self):
        self.eyes.close()
        self.gaze.shutdown()


    def load_plugins(self):
        for name, plug in find_phal_plugins().items():
            config = self.config.get(name) or {}
            if hasattr(plug, "validator"):
                enabled = plug.validator.validate(config)
            else:
                enabled = config.get("enabled")
            if enabled:
                try:
                    self.drivers[name] = plug(bus=self.bus, config=config)
                    LOG.info(f"PHAL plugin loaded: {name}")
                except Exception:
                    LOG.exception(f"failed to load PHAL plugin: {name}")
                    continue

    def start(self):
        self.status.set_started()
        try:
            self.load_plugins()
            self.status.set_ready()
            self.eyes.reset()
        except Exception as e:
            LOG.exception(e)
            self.status.set_error(e)

    def shutdown(self):
        self.status.set_stopping()
