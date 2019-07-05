"""
HA Connector
Copyright (c) 2018 fison67 <fison67@nate.com>
Licensed under MIT
following to your configuration.yaml file.
ha_connector:
  app_url: xxx
  app_id: xxx
  access_token: xxxxxx
  target_devices:
    - device_id1
    - device_id2
    ...
"""
import requests
import logging

import homeassistant.loader as loader
from homeassistant.const import (STATE_UNKNOWN, EVENT_STATE_CHANGED)
#from homeassistant.remote import JSONEncoder

_LOGGER = logging.getLogger(__name__)

DOMAIN = "ha_connector"

def setup(hass, config):
    app_url = config[DOMAIN].get('app_url')
    app_id = config[DOMAIN].get('app_id')
    access_token = config[DOMAIN].get('access_token')
    target_devices = config[DOMAIN].get('target_devices')
    
    def event_listener(event):

        state = event.data.get('new_state')
        if state is None or state.state in (STATE_UNKNOWN, ''):
            return None

        jsonData = {};
        newState = event.data['new_state'];
        if newState is None:
            return;
        
        if newState.entity_id not in target_devices:
            return;
        
#        oldState = event.data['old_state'];
#        if oldState is None:
#          return;

        url = app_url + app_id + "/update?access_token=" + access_token + "&entity_id=" + newState.entity_id + "&value=" + newState.state;
        try:
           if newState.attributes.unit_of_measurement:
              url += "&unit=" + newState.attributes.unit_of_measurement
        except:
           url = url

        response = requests.get(url);
        _LOGGER.debug(str(response) +" : " +url)
    hass.bus.listen(EVENT_STATE_CHANGED, event_listener)

    return True
