from os.path import dirname, join
import milight

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger

__author__ = 'mgoriup'

LOGGER = getLogger(__name__)

class MilightSkill(MycroftSkill):
    def __init__(self):
        super(MilightSkill, self).__init__(name="MilightSkill")
        self.host = str(self.config['host'])
        self.port = int(self.config['port'])

        self.controller = milight.MiLight({'host': self.host, 'port': self.port},
                                           wait_duration=0)
        self.light = milight.LightBulb(['rgbw', 'white', 'rgb']) #will read zone parameter

    def initialize(self):
        self.load_vocab_files(join(dirname(__file__), 'vocab', self.lang))
        self.load_regex_files(join(dirname(__file__), 'regex', self.lang))
        
        light_on = IntentBuilder("LightOnIntent").require(
            "LightKeyword").require("OnKeyword").require("LightZone").build()
        self.register_intent(light_on, self.handle_light_on)
        
        all_light_on = IntentBuilder("AllLightOnIntent").require(
            "LightKeyword").require("AllKeyword").require("OnKeyword").build()
        self.register_intent(all_light_on, self.handle_all_light_on)
        
        light_off = IntentBuilder("LightOffIntent").require(
            "LightKeyword").require("OffKeyword").require("LightZone").build()
        self.register_intent(light_off, self.handle_light_off)        
        
        all_light_off = IntentBuilder("AllLightOffIntent").require(
            "LightKeyword").require("AllKeyword").require("OffKeyword").build()
        self.register_intent(all_light_off, self.handle_all_light_off)
        
        light_white = IntentBuilder("LightWhiteIntent").require(
            "LightKeyword").require("WhiteKeyword").require("LightZone").build()
        self.register_intent(light_white, self.handle_light_white)
        
        night_light = IntentBuilder("NightLightIntent").require(
            "NightKeyword").require("LightKeyword").require("LightZone").build()
        self.register_intent(night_light, self.handle_night_light)
        
        light_color = IntentBuilder("LightColorIntent").require(
            "LightKeyword").require("Color").require("LightZone").build()
        self.register_intent(light_color, self.handle_light_color)
        
        light_brightness = IntentBuilder("LightBrightnessIntent").require(
            "LightKeyword").require("BrightnessKeyword").require(
                "Brightness").require("LightZone").build()
        self.register_intent(light_brightness, self.handle_light_brightness)

    def handle_light_on(self, message):
        light_zone = message.metadata.get('LightZone')
        try:
            self.controller.send(self.light.on(light_zone))
        except Exception as e:
            LOGGER.error("Error: {0}".format(e))

    def handle_all_light_on(self, message):
        try:
            self.controller.send(self.light.all_on())
        except Exception as e:
            LOGGER.error("Error: {0}".format(e))

    def handle_light_off(self, message):
        light_zone = message.metadata.get('LightZone')
        try:
            self.controller.send(self.light.off(light_zone))
        except Exception as e:
            LOGGER.error("Error: {0}".format(e))

    def handle_all_light_off(self, message):
        try:
            self.controller.send(self.light.all_off())
        except Exception as e:
            LOGGER.error("Error: {0}".format(e))

    def handle_light_white(self, message):
        light_zone = message.metadata.get('LightZone')
        try:
            self.controller.send(self.light.white(light_zone))
        except Exception as e:
            LOGGER.error("Error: {0}".format(e))

    def handle_night_light(self, message):
        light_zone = message.metadata.get('LightZone')
        try:
            self.controller.send(self.light.night(light_zone))
        except Exception as e:
            LOGGER.error("Error: {0}".format(e))
            
    def handle_light_color(self, message):
        color = message.metadata.get("Color")
        light_zone = message.metadata.get("LigtZone")
        try:
            self.controller.send(self.light.color(color, light_zone))
        except Exception as e:
            LOGGER.error("Error: {0}".format(e))

    def handle_light_brightness(self, message):
        brightness_level = message.metadata.get("Brightness")
        light_zone = message.metadata.get("LightZone")
        if brightness not in range (0,101):
            self.speak_dialog(
                "the.light.brightness.must.be.between.one.and.one.hundred")
        else:
             self.controller.send(self.light.brightness(brightness_level,
                                                            light_zone))
        #will add exception
        
    def stop(self):
        pass
    
def create_skill():
    return MilightSkill()