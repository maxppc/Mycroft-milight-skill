# Mycroft-milight-skill

# Description
Mycroft Skill to control smart light bulbs of the following brands:
* MiLight
* LimitlessLED
* AppLight
* AppLamp
* LEDme
* dekolight
* iLight
* EasyBulb
Full API documentation can be found here: http://www.limitlessled.com/dev/

# Requirements:
```.py
pip install milight
```
Thanks to https://github.com/McSwindler/python-milight

# Setup:
Edit mycroft.ini to add MilightSkill section
```
[MilightSkill]
host = your_hub_ip
port = _port_ #default 8899
```

# Usage:
```
Mycroft, lights all on
Mycroft, switch on first zone
etc
```
