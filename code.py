#@author Dove Thompson
#@version 1.0
#Purpose: interface with the hid_gamepad class to make a simple 2 axis analog input for logitech g27 racing pedals
import board
import digitalio
import analogio
import usb_hid
import time
from hid_gamepad import Gamepad

class SmoothingManager:#class to manage averaging of past data points to make input less jittery
    def __init__(self):
        self.buffer = []

    def update_data(self, xval):
        self.buffer.append(xval)
        if len(self.buffer) > 10:#change this value to change the ammount of smoothing happening!
            self.buffer.pop(0)  #remove the oldest element if buffer size exceeds desired smoothing ammount

    def smooth(self):
        buffer_sum = sum(self.buffer)
        return int(buffer_sum / len(self.buffer)) if self.buffer else 0

def map_range(value, from_low, from_high, to_low, to_high):
    """Map a value from one range to another."""
    current_map = int((value - from_low) * (to_high - to_low) / (from_high - from_low) + to_low)
    if current_map <= -114:#prevent value from exceeding hid limit and crashing
        return -127
    elif current_map >= 120:#make input return to 0 when close 
        return 127
    else:
        return current_map

gp = Gamepad(usb_hid.devices)

ax = analogio.AnalogIn(board.GP26)
bx = analogio.AnalogIn(board.GP27)

smoother_a = SmoothingManager()#create instance of smoothing manager class for a
smoother_b = SmoothingManager()#create instance of smoothing manager class for b

# Main loop
while True:
    # Read analog input values
    ax_value = ax.value
    bx_value = bx.value

    # Map analog input values to gamepad axes
    ax_mapped = map_range(ax_value, 200, 55000, -127, 127)#adjust values to calibrate pots
    bx_mapped = map_range(bx_value, 5000, 60000, -127, 127)

    #smooth analog inputs
    smoother_a.update_data(ax_mapped)
    smoother_b.update_data(bx_mapped)

    ax_smooth = smoother_a.smooth()
    bx_smooth = smoother_b.smooth()

    # Update gamepad axes
    gp.move_joysticks(x=ax_smooth, y=bx_smooth)

    #print(str(ax_value) + " " + str(bx_value))#debug statments!
    #print()
    #print(str(ax_mapped) + " " + str(bx_mapped))
    #print()
    #print(str(ax_smooth) + " " + str(bx_smooth))
    #print()
    #time.sleep(.1)#makes debug out more readable at cost of input lag
