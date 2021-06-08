# Macro-Zero
From prototype to production, macro keyboard utilizing power of a Raspberry Pi to take DIY to a whole new level. Designed around the Raspberry Pi Zero.

## Vision
The idea behind this device is to create a macro-board to assist with tasks that are repeative or tedious while adding some cool features in a small form factor.

[![Application Testing Workflow](https://github.com/dwmoffatt/macro-zero/workflows/Application%20Testing/badge.svg?branch=master)](https://github.com/dwmoffatt/macro-zero/actions?query=workflow%3AApplication%20Testing)
[![Code style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

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
##### Configuration Loading
Button configuration will be loadable. File format will be JSON. File name needed is `macro-zero configuration.json`. Config file needs to be stored in `src/configs`. If no config file is present then default/example config will be loaded from `src/configs`. Default/example config file name is `macro-zero default configuration.json`.  Each mode will have a definition for each button. Within th button definition there will be 3 fields: `CommandName`, `CommandInterval`, `Commands`. `CommandName` is the name that will displayed for the command and is limited to 10 characters.  `CommandInterval` this is the time in seconds to delay between sending commands to the host if more then 1 Command is present in the `Commands` field.
`Commands` is a list of command, each command containing a type and a command. Supported types: `Command String`, `Keyboard Function`. `Command String` is a string you want to appear on the connected device. `Keyboard Function` is used to specify a specific keyboard function you want press, ie. Enter Key, Function Keys, Backspace, Tab, etc.
```
{
   "General": {
      "B1": {
         "CommandName": "Hello World",
         "CommandInterval": 1,
         "Commands": [
            {
               "Type": "Command String",
               "Command": "Hello World!!"
            }
         ]
      },
      "B2": {
         "CommandName": "N/A",
         "CommandInterval": 1,
         "Commands": []
      },
      "B3": {
         "CommandName": "N/A",
         "CommandInterval": 1,
         "Commands": []
      },
      "B4": {
         "CommandName": "N/A",
         "CommandInterval": 1,
         "Commands": []
      },
      "B5": {
         "CommandName": "N/A",
         "CommandInterval": 1,
         "Commands": []
      },
      "B6": {
         "CommandName": "Git Status",
         "CommandInterval": 1,
         "Commands": [
            {
               "Type": "Command String",
               "Command": "git status"
            },
            {
               "Type": "Keyboard Function",
               "Command": "Enter"
            }
         ]
      },
      "B7": {
         "CommandName": "Git Pull",
         "CommandInterval": 1,
         "Commands": [
            {
               "Type": "Command String",
               "Command": "git pull"
            },
            {
               "Type": "Keyboard Function",
               "Command": "Enter"
            }
         ]
      },
      "B8": {
         "CommandName": "Shutdown",
         "CommandInterval": 1,
         "Commands": [
            {
               "Type": "Command String",
               "Command": "sudo shutdown"
            }
         ]
      }
   },
   "Macro-Zero": {
      "B1": {
         "CommandName": "cdc_ether",
         "CommandInterval": 1,
         "Commands": [
            {
               "Type": "Command String",
               "Command": "dmesg | grep cdc_ether"
            },
            {
               "Type": "Keyboard Function",
               "Command": "Enter"
            }
         ]
      },
      "B2": {
         "CommandName": "En. Inet Sharing",
         "CommandInterval": 10,
         "Commands": [
            {
               "Type": "Command String",
               "Command": "echo 1 | sudo tee /proc/sys/net/ipv4/ip_forward > /dev/null"
            },
            {
               "Type": "Command String",
               "Command": "sudo iptables -P FORWARD ACCEPT"
            },
            {
               "Type": "Command String",
               "Command": "sudo iptables -A POSTROUTING -t nat -j MASQUERADE -s 10.0.0.1/24"
            }
         ]
      },
      "B3": {
         "CommandName": "Dis. Inet Sharing",
         "CommandInterval": 10,
         "Commands": [
            {
               "Type": "Command String",
               "Command": "echo 0 | sudo tee /proc/sys/net/ipv4/ip_forward > /dev/null"
            },
            {
               "Type": "Command String",
               "Command": "sudo iptables -t nat -F POSTROUTING"
            }
         ]
      },
      "B4": {
         "CommandName": "N/A",
         "CommandInterval": 1,
         "Commands": []
      },
      "B5": {
         "CommandName": "N/A",
         "CommandInterval": 1,
         "Commands": []
      },
      "B6": {
         "CommandName": "N/A",
         "CommandInterval": 1,
         "Commands": []
      },
      "B7": {
         "CommandName": "N/A",
         "CommandInterval": 1,
         "Commands": []
      },
      "B8": {
         "CommandName": "N/A",
         "CommandInterval": 1,
         "Commands": []
      }
   }
}
```

##### Testing
`python3 -m pytest --cov-report html:cov_html --cov=src tests/`

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
MK_B6       | 40
MK_B7       | 38
MK_B8       | 36

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
4. cd to scripts and run `./install.sh all`

### Linux
#### Installing deps
`./install.sh depsonly`

#### Setup NIC and setup Internet Sharing
##### On Host
###### Enable USB NIC
`dmesg | grep cdc_ether` use to see what your cdc_ether NIC is setup as\
`sudo ifconfig {NIC returned from ^} 10.0.0.2 netmask 255.255.255.252 up` use to enable NIC
###### Enable Internet Sharing
`echo 1 | sudo tee /proc/sys/net/ipv4/ip_forward > /dev/null`\
`sudo iptables -P FORWARD ACCEPT`\
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

https://www.digitalocean.com/community/tutorials/how-to-use-systemctl-to-manage-systemd-services-and-units

https://www.digitalocean.com/community/tutorials/understanding-systemd-units-and-unit-files

https://www.tutorialspoint.com/python_pillow/python_pillow_quick_guide.htm

https://gist.github.com/MightyPork/6da26e382a7ad91b5496ee55fdc73db2

https://www.freedesktop.org/software/systemd/man/systemd.unit.html

https://www.tutorialspoint.com/flask/index.htm

https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world

https://www.raspberrypi-spy.co.uk/2013/07/how-to-use-a-mcp23017-i2c-port-expander-with-the-raspberry-pi-part-2/

https://pypi.org/project/smbus2/

https://ww1.microchip.com/downloads/en/devicedoc/20001952c.pdf
