make sure to get the hid library: https://github.com/adafruit/Adafruit_CircuitPython_HID

1: copy the code.py, boot.py and hid_gamepad.py to the pico.
2: install the hid library in the lib folder
3: unmount, and reconnect pico, device should appear as hid device with an x and y axis

Read comments in code.py for help adjusting the inputs for your potentiometers

todo:
add rudder mode for MSFS
validate on windows (software was tested on linux)
remove phantom buttons and inputs from hid properties (without breaking everything)
