# macro-zero
From prototype to production, macro keyboard utilizing power of a raspberry-pi to take DIY to a whole new level. Designed around the raspberry pi zero.

# Design
Parts:
- raspberry pi zero
- e-ink display https://www.waveshare.com/wiki/2.13inch_e-Paper_HAT
- 9 mechanical switches - 9 Inputs
- 2 rotary encoders - 6 Inputs
- MCP23017 I2C 16 I/O Expander 

# Setup
## Linux
`dmesg|grep cdc_ether` use to see what your cdc_ether NIC is setup as
`sudo ifconfig {NIC returned from ^} 10.0.0.2 netmask 255.255.255.252 up` use to enable NIC

# Reference Material
https://www.rmedgar.com/blog/using-rpi-zero-as-keyboard-setup-and-device-definition/

https://eleccelerator.com/tutorial-about-usb-hid-report-descriptors/

http://www.isticktoit.net/?p=1383

https://irq5.io/2016/12/22/raspberry-pi-zero-as-multiple-usb-gadgets/

https://andrewnicolaou.co.uk/posts/2016/pi-zero-midi-3-two-things-at-once
