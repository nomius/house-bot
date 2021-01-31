#!/usr/bin/env python

import requests
import time

from midea.client import client as midea_client
from midea.device import air_conditioning_device as ac

import logging

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

import config

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

class Temperatures(object):
    FROM = "tuya"
    TUYACLOUDURL = "https://px1.tuya{}.com"
    current_token = ""

    midea_client = type('', (), {})()

    def get_tuya_token(self, get_new=False):
        if self.current_token == "" or get_new:
            auth_response = requests.post((self.TUYACLOUDURL + "/homeassistant/auth.do").format(config.TUYA_API_REGION),
                data = {
                    "userName": config.TUYA_USERNAME,
                    "password": config.TUYA_PASSWORD,
                    "countryCode": config.TUYA_COUNTRY_CODE,
                    "bizType": config.TUYA_BIZ_TYPE,
                    "from": self.FROM,
                },
            )
            auth_response = auth_response.json()
            if auth_response.get('errorMsg') == 'you cannot auth exceed once in 60 seconds':
                time.sleep(62)
                return self.get_tuya_token(get_new=True)
            return auth_response["access_token"]
        return current_token


    def get_current_upper_floor_temperature(self):
        header = { "name": "Discovery", "namespace": "discovery", "payloadVersion": 1 }
        token = self.get_tuya_token(get_new=False)
        payload = { "accessToken": token }
        data = { "header": header, "payload": payload }
        try:
            discovery_response = requests.post((self.TUYACLOUDURL + "/homeassistant/skill").format(config.TUYA_API_REGION), json=data)
        except:
            token = self.get_tuya_token(get_new=True)
            discovery_response = requests.post((self.TUYACLOUDURL + "/homeassistant/skill").format(config.TUYA_API_REGION), json=data)
        discovery_response = discovery_response.json()
        return { "current_temperature" : float(discovery_response['payload']['devices'][0]['data']['current_temperature'])/10, "winter_heating_temperature" : float(discovery_response['payload']['devices'][0]['data']['temperature'])/10}

    def midea_session(self):
        self.midea_client = midea_client(config.MIDEA_API_KEY, config.MIDEA_USERNAME, config.MIDEA_PASSWORD)
        self.midea_client.setup()

    def get_current_lower_floor_temperatures(self):
        try:
            device = self.midea_client.devices()[0]
            device.refresh()
        except:
            self.midea_session()
            device = self.midea_client.devices()[0]
            device.refresh()
        return { "indoor_temperature" : device.indoor_temperature, "outdoor_temperature" : device.outdoor_temperature }

temperatures = Temperatures()

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hi, I\'m DaveC bot.')

def temperatures_command(update: Update, context: CallbackContext) -> None:
    t_up = temperatures.get_current_upper_floor_temperature()
    t_low = temperatures.get_current_lower_floor_temperatures()
    update.message.reply_text(
        ('Current upper floor temperature is: {}ºC\n'
         'Current lower floor temperature is: {}ºC\n'
         'Current outdoor temperate is: {} ºC\n'
         'Winter automatic heating temperature is setup at: {}ºC')
        .format(
             t_up['current_temperature'],
             t_low['indoor_temperature'],
             t_low['outdoor_temperature'],
             t_up['winter_heating_temperature']
        )
    )

def main():
    updater = Updater(config.TELEGRAM_BOT_KEY, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("temperatures", temperatures_command))

    #dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()

