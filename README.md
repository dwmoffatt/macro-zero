# macro-zero
From prototype to production, macro keyboard utilizing power of a raspberry-pi to take DIY to a whole new level. Designed around the raspberry pi zero.

## Vision
The idea behind this device is to create a macro-board to assist with tasks that are repeative or tedious while adding some cool features in a small form factor. 8 macro keys, a rotary encoder and a display to show options. The one rotary encoder will be used to switch modes and add some features in each mode.

## Design
### Software
Main script:\
should run device interface without exiting\
Modules:\
specific modules for hard interfaces on the device\
each module will contain a module_init() and a module_close()\
Module `__init__`:
- input_list - list of dictionaries - Input
- thread_lock - Thread Lock object reference - Input
- que - Input que - Output
###### input_list dictionary struct:
```
{ 
   "InputType": "Button",
   "PinNumber": 22
}
```

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
- 1 rotary encoder - 3 Inputs
- 1 Supercap backup module with 1 switch sense input
- MCP23017 I2C 16 I/O Expander

##### I/O Mapping:
I/O Function| Board Pin Number
------------|-----------------
MOSI        | 19 *
SCLK        | 23 *
CS          | 24 *
DC          | 18
RST         | 22
SDA         | 3  **
SCL         | 5  **
PSO         | 16 ***
RE_SW       | 11
RE_CLK      | 13
RE_DR       | 15
MK_B1       | 29
MK_B2       | 31
MK_B3       | 33
MK_B4       | 35
MK_B5       | 37
MK_B6       | 36
MK_B7       | 38
MK_B8       | 40

\* I/O is part of SPI. Declared in python library. No need to configure\
** I2C interface. Declared in python library. No need to configure\
*** PSO = Power Switch Over, used to tell when device has lost power over usb. Start shutdown sequence\
https://pinout.xyz/#

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
###### Give pi permission to hidg0
`sudo chown pi:root /dev/hidg0`
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

https://everyday.codes/linux/services-in-systemd-in-depth-tutorial/
