# macro-zero
From prototype to production, macro keyboard utilizing power of a raspberry-pi to take DIY to a whole new level. Designed around the raspberry pi zero.

## Vision
The idea behind this device is to create a macro-board to assist with tasks that are repeative or tedious while adding some cool features in a small form factor. 8 macro keys with 2 rotary encoders and a display to show options. One rotatry encoder will be to switch between modes changing what each of the 8 macro keys does. The other rotary encoder will add additonal features on top of the 8 macro keys per mode.

## Design
### Software
Main script:\
should run device interface without exiting\
Modules:\
specific modules for hard interfaces on the device\
each module will contain a module_init() and a module_close()
### Hardware
##### Board Size:
80mm (w) x 100mm (L)

##### Design Restrictions:
Max size of PCB: 100mm by 100mm due to cost\
3D printer build area: 130mm (L) x 80mm (W) x 165mm（H）\
Limit to 450mA draw from usb port

##### Parts:
- raspberry pi zero
- display
- 8 mechanical switches - 8 Inputs
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
#### Required python modules
python3 is used. Required modules below:\
`sudo apt-get install python3-pip`\
`sudo apt-get install python3-pil`\
`sudo apt-get install python3-numpy`\
`sudo pip3 install RPi.GPIO`\
`sudo pip3 install spidev`\
`sudo apt-get install python3-smbus`\

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

https://andrewnicolaou.co.uk/posts/2016/pi-zero-midi-3-two-things-at-once

https://shallowsky.com/blog/linux/raspberry-pi-ethernet-gadget-2.html

https://developer.ridgerun.com/wiki/index.php/How_to_use_USB_device_networking
