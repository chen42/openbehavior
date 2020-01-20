
Use USB RFID reader

need to enable 1-wire and serial in raspi-config

Add the followig lines to /boot/config.txt

```
 # for external temp probe
dtoverlay=w1-gpio
dtoverlay=pi3-disable-bt

```
