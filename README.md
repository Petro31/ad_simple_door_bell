# Home Assistant Simple Doorbell Notification & TTS

[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg?style=for-the-badge)](https://github.com/custom-components/hacs)
<br><a href="https://www.buymeacoffee.com/Petro31" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-black.png" width="150px" height="35px" alt="Buy Me A Coffee" style="height: 35px !important;width: 150px !important;" ></a>

_Simple Door Bell app for AppDaemon._

This notifies you when the doorbell rings. 

## Installation

Download the `simple_door_bell` directory from inside the `apps` directory to your local `apps` directory, then add the configuration to enable the `hacs` module.

## Example App configuration

#### Notifications only
```yaml
door_bell:
  module: simple_door_bell
  class: DoorBell
  sensor: binary_sensor.doorbell_button
  notify:
  - notify.petro
```

#### Advanced 
```yaml
# Creates all notifications
door_bell:
  module: simple_door_bell
  class: DoorBell
  sensor: binary_sensor.doorbell_button
  timestamp: '%-I:%M:%S %p'
  notify:
  - notify.petro
  tts_services:
  - service: notify.alexa_media
    data:
      data:
        type: announce
      target: 
      - media_player.dot1
      - media_player.dot2
```

#### App Configuration
key | optional | type | default | description
-- | -- | -- | -- | --
`module` | False | string | `simple_door_bell` | The module name of the app.
`class` | False | string | `DoorBell` | The name of the Class.
`sensor` | False | string | | entity_id of the door bell sensor.
`message`| True | string | `Door Bell!` | Message for the notification and TTS (if message is omitted from TTS data).
`notify` | True | list | | Notification list for simple message.
`timestamp` | True | string | | Timestamp format for messages.  Use `'%-I:%M:%S %p'` for 12 hr notation and `'%-H:%M:%S'` for 24 hr 
`tts_services` | True | list | | List of TTS services.
`title` | True | string | | Title for the notifications.
`log_level` | True | `'INFO'` &#124; `'DEBUG'` | `'DEBUG'` | Switches log level.

#### TTS Map Configuration
key | optional | type | default | description
-- | -- | -- | -- | --
`service` | False | string | | Name of the service.
`data` | True | dict | | Data that accompanies the service.
