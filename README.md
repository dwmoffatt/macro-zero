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
##### Configuration Loading
Button configuration will be loadable. File format will be JSON. File name needed is `macro-zero configuration.json`. Config file needs to be stored in `src/configs`. If no config file is present then default/example config will be loaded from `src/configs`. Default/example config file name is `macro-zero default configuration.json`.  Each mode will have a definition for each button. Within th button definition there will be 3 fields: `CommandName`, `CommandInterval`, `Commands`. `CommandName` is the name that will displayed for the command and is limited to 10 characters.  `CommandInterval` this is the time in seconds to delay between sending commands to the host if more then 1 Command is present in the `Commands` field.
`Commands` is a list of command, each command containing a type and a command. Supported types: `Command String`, `Keyboard Function`. `Command String` is a string you want to appear on the connected device. `Keyboard Function` is used to specify a specific keyboard function you want press, ie. Enter Key, Function Keys, Backspace, Tab, etc.
```
{
   "General": {
      "B1": {
         "CommandName": "N/A",
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
         "CommandInterval": 15,
         "Commands": [
            {
               "Type": "Command String",
               "Command": "echo 1 | sudo tee /proc/sys/net/ipv4/ip_forward > /dev/null"
            },
            {
               "Type": "Command String",
               "Command": "sudo iptables -A POSTROUTING -t nat -j MASQUERADE -s 10.0.0.1/24"
            }
         ]
      },
      "B3": {
         "CommandName": "Dis. Inet Sharing",
         "CommandInterval": 15,
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
`python3 -m unittest discover -v -s src/tests/unit/app/`\
`python3 -m unittest discover -v -s src/tests/unit/mkeyboard/`

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
4. copy `macro-zero` bash script to `/usr/bin` on device rootfs
5. make it executable `sudo chmod +x /usr/bin/macro-zero`

### Linux
#### Required python modules
python3 is used. Required modules below:\
`sudo apt install python3-pip`\
`sudo apt install libopenjp2-7-dev`\
`pip3 install --upgrade pip`\
`pip3 install -r requirements.txt`

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
###### Give pi permission to hidg0
`sudo chown pi:root /dev/hidg0`

## Reference Material
https://www.rmedgar.com/blog/using-rpi-zero-as-keyboard-setup-and-device-definition/

https://eleccelerator.com/tutorial-about-usb-hid-report-descriptors/

http://www.isticktoit.net/?p=1383

https://andrewnicolaou.co.uk/posts/2016/pi-zero-midi-3-two-things-at-once

https://shallowsky.com/blog/linux/raspberry-pi-ethernet-gadget-2.html

https://developer.ridgerun.com/wiki/index.php/How_to_use_USB_device_networking

https://everyday.codes/linux/services-in-systemd-in-depth-tutorial/

https://www.tutorialspoint.com/python_pillow/python_pillow_quick_guide.htm

https://gist.github.com/MightyPork/6da26e382a7ad91b5496ee55fdc73db2
