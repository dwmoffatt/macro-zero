# macro-zero
From prototype to production, macro keyboard utilizing power of a raspberry-pi to take DIY to a whole new level. Designed around the raspberry pi zero.

## Design
Parts:
- raspberry pi zero
- e-ink display https://www.waveshare.com/wiki/2.13inch_e-Paper_HAT
- 9 mechanical switches - 9 Inputs
- 2 rotary encoders - 6 Inputs
- MCP23017 I2C 16 I/O Expander 

## Setup Ethernet Keyboard Gadget
1. Add `dtoverlay=dwc2` at the end of ` boot/config.txt`
2. And the following two lines at the end of `/etc/modules` on device rootfs
   ```
   dwc2
   libcomposite
   ```
4. copy `macro-zero` bash script to `/usr/bin` on device rootfs
5. make it executable `sudo chmod +x /usr/bin/macro-zero`

### Linux
#### Setup NIC and setup Internet Sharing
##### On Host
###### Enable USB NIC
`dmesg | grep cdc_ether` use to see what your cdc_ether NIC is setup as\
`sudo ifconfig {NIC returned from ^} 10.0.0.2 netmask 255.255.255.252 up` use to enable NIC
###### Enable Internet Sharing
`echo 1 | sudo tee /proc/sys/net/ipv4/ip_forward > /dev/null`\
`sudo iptables -A POSTROUTING -t nat -j MASQUERADE -s 10.0.0.1/24`
###### Disable Internet Sharing
`echo 0 | sudo tee /proc/sys/net/ipv4/ip_forward > /dev/null`\
`sudo iptables -t nat -F POSTROUTING`
##### On Device
This is due to Gateway not being setup properly on startup\
`sudo route del default`\
`sudo route add default gw 10.0.0.2`

## Reference Material
https://www.rmedgar.com/blog/using-rpi-zero-as-keyboard-setup-and-device-definition/

https://eleccelerator.com/tutorial-about-usb-hid-report-descriptors/

http://www.isticktoit.net/?p=1383

https://irq5.io/2016/12/22/raspberry-pi-zero-as-multiple-usb-gadgets/

https://andrewnicolaou.co.uk/posts/2016/pi-zero-midi-3-two-things-at-once

https://shallowsky.com/blog/linux/raspberry-pi-ethernet-gadget-2.html

https://developer.ridgerun.com/wiki/index.php/How_to_use_USB_device_networking
