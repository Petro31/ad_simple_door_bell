import appdaemon.plugins.hass.hassapi as hass
import voluptuous as vol
from datetime import datetime

MODULE = 'simple_door_bell'
CLASS = 'DoorBell'
DOMAIN = 'domain'
SERVICE = 'service'

CONF_MODULE = 'module'
CONF_CLASS = 'class'
CONF_DATA = 'data'
CONF_SENSOR = 'sensor'
CONF_NOTIFY = "notify"
CONF_TTS_SERVICES = 'tts_services'
CONF_MESSAGE = 'message'
CONF_SERVICE = 'service'
CONF_TIMESTAMP = 'timestamp'
CONF_TITLE = 'title'
CONF_TTS = 'tts_message'
CONF_LOG_LEVEL = 'log_level'

LOG_DEBUG = 'DEBUG'
LOG_ERROR = 'ERROR'
LOG_INFO = 'INFO'
LOG_WARNING = 'WARNING'

STATE_ON = 'on'
STATE_OFF = 'off'

TTS_SCHEMA = vol.Schema({
    vol.Required(CONF_SERVICE): str,
    vol.Optional(CONF_DATA):dict,
})

APP_SCHEMA = vol.Schema({
    vol.Required(CONF_MODULE): MODULE,
    vol.Required(CONF_CLASS): CLASS,
    vol.Required(CONF_SENSOR): str,
    vol.Optional(CONF_NOTIFY, []): [str],
    vol.Optional(CONF_TTS_SERVICES, []): [TTS_SCHEMA],
    vol.Optional(CONF_TITLE): str,
    vol.Optional(CONF_MESSAGE): str,
    vol.Optional(CONF_TIMESTAMP): str,
    vol.Optional(CONF_LOG_LEVEL, default=LOG_DEBUG): vol.Any(LOG_INFO, LOG_DEBUG),
    })

class DoorBell(hass.Hass):
    def initialize(self):
        args = APP_SCHEMA(self.args)

        # Set Lazy Logging (to not have to restart appdaemon)
        self._level = args.get(CONF_LOG_LEVEL)
        self.log(args, level=self._level) 

        self._services = [ service[SERVICE] for service in self.list_services(namespace="default") if service[DOMAIN] == CONF_NOTIFY ]
        self.log(f"Notify services {self._services}", level = self._level)

        # iterate through notify list and get the valid notify calls.
        self._notify, invalid = self.parse_notify(args.get(CONF_NOTIFY))

        self._sensor = args.get(CONF_SENSOR)
        
        self._message = args.get(CONF_MESSAGE, "Door Bell!")

        self._tts_services = [ AppService(c, self._message) for c in args.get(CONF_TTS_SERVICES) ]

        self._title = args.get(CONF_TITLE, "")

        self._timestamp = args.get(CONF_TIMESTAMP, "")

        self._tts = args.get(CONF_TTS, self._message)

        self.handle = self.listen_state(self.track_sensor, entity = self._sensor, new=STATE_ON)

    def track_sensor(self, entity, attribute, old, new, kwargs):
        if self._notify:
            data = {}
            if self._title:
                data[CONF_TITLE] = self._title
            
            if self._timestamp:
                dt = datetime.now()
                message = f"[{dt.strftime(self._timestamp)}] {self._message}"
            else:
                message = self._message

            for n in self._notify:
                data['name'] = n
                self.log(f"Notifying '{n}': '{message}'", level = self._level)
                self.notify(message, **data)

        if self._tts_services:
            for service in self._tts_services:
                self.log(f"Announcing to {service.tostring()}", level = self._level)
                self.call_service(service.call, **service.data)

    def terminate(self):
        self.log(f"Canceling handle '{self.handle}'", level=self._level)
        self.cancel_listen_event(self.handle)

    def parse_notify(self, notify_list):
        good, bad = [], []
        for n in notify_list:
            if n.startswith(CONF_NOTIFY) and n.count('.') == 1:
                n = n.split('.')[-1]
            if n in self._services:
                good.append(n)
            else:
                bad.append(n)
        return good, bad

class AppService(object):
    def __init__(self, conf, message):
        self._service = conf.get(CONF_SERVICE)
        self._data = conf.get(CONF_DATA)

        if CONF_MESSAGE not in self._data:
            self._data[CONF_MESSAGE] = message

    @property
    def service(self): return self._service

    @property
    def data(self): return self._data

    @property
    def call(self): return self._service.replace('.', '/')

    def tostring(self): return f"'{self.service}' - {self.data}"
