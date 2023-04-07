# DESKY HOME ASSISTANT INTEGRATION

###WARNING! WORK IN PROGRESS! INTEGRATION STILL UNSTABLE AND BUGGY!! USE UNDER YOUR OWN RESPONSABILITY!!

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg?style=for-the-badge)](https://github.com/hacs/integration)

This component provides integration with the amazing job that [Stefichen5](https://github.com/Stefichen5/AutonomousControl) and [developit](https://github.com/developit/desky) did to reverse-engineering and create a light API to control Autonomous desks.

## How to install
You can use HACS to install this integration as custom repository

If you are not using HACS, you must copy `desky` folder into your `custom_components` folder

## Configuration
Configuration via integration is recommended. Add an instance of `desky-ha` using the UI and provide a name for the instance and the url to connect (eg: `http://192.168.1.1`)


## Screenshot
Integration will create a device with a number entity, 4 buttons (one for each memory) and a sensor
![](https://github.com/vipial1/desky-ha/blob/main/images/example.png?raw=true)


## Work in progress
- This is just a MVP, so everything is still in progress
- Complete this readme with more useful information

## Thanks to
- [Stefichen5](https://github.com/Stefichen5/AutonomousControl) and [developit](https://github.com/developit/desky) for the amazing job they did to reverse-engineering and create a light API to control Autonomous desks.


## Long history about how I made this work (almost like a blog)
After several hours reading documentation from Stefichen5 and developit, I bought a [ESP8266](https://amzn.eu/d/1e0mKDJ) and a [10P10C cable](https://amzn.eu/d/iLLwiH6) that will allow us to use both the ESP8266 and the table controller.

Quite hard job to flash the ESP8266 (better read the docu) and push the code from developit (file missing that he kindly uploaded).

Time to cut cables:
![](https://github.com/vipial1/desky-ha/blob/main/images/cables.png?raw=true)

and create an ugly prototype to see if it works:
![](https://github.com/vipial1/desky-ha/blob/main/images/proto.png?raw=true)

how do I know which cable is what? by comparing it with cable coming from the controler, so the correspondence is:

| Color  | PIN |
|--------|-----|
| Grey   | TX  |
| Purple | RX  |
| White  | 5V  |
| Blue   | GND |

At this point, I expended a lot of time investigating why it doesn't work, and the answer is: SERIAL PORT!! it is not posible to get power suply from usb and transmit data using TX and RX ports...solution is obvious: take the power from the desk itself.

Ok, now desk can be moved from the ESP8266 but not from the original controler. Well, make sense, it is a bus, it is not designed for that...how do we solve it? With a [diode](https://amzn.eu/d/cpcBqgH). A diode is the electronic equivalent of a valve, it allows to flow the electricity in only one direction, so, it allow us to have to sources writing to a bus without causing problems. Simply add the diode after the TX PIN in the ESP8266.


Et voilà!! it works! we can use both the desk controller and the ESP8266 at same time!!


Time to make a nicer prototype and put it inside a case. 

Final result:
![](https://github.com/vipial1/desky-ha/blob/main/images/final.png?raw=true)


