#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
import datetime

# Set BOARD mode
GPIO.setmode(GPIO.BOARD)

# Disable warnings
GPIO.setwarnings(False)

# Set pins for 74HC595
data_pin = 23
clock_pin = 19
latch_pin = 21

# Set list for digit segment in 8 bit. Inverted Values!
#  AAA
# F   B
# F   B
# F   B
#  GGG
# E   C
# E   C
# E   C
#  DDD .

digit = {
    #       . G F E D C B A
    0:     [1,1,0,0,0,0,0,0],
    1:     [1,1,1,1,1,0,0,1],
    2:     [1,0,1,0,0,1,0,0],
    3:     [1,0,1,1,0,0,0,0],
    4:     [1,0,0,1,1,0,0,1],
    5:     [1,0,0,1,0,0,1,0],
    6:     [1,0,0,0,0,0,1,0],
    7:     [1,1,1,1,1,0,0,0],
    8:     [1,0,0,0,0,0,0,0],
    9:     [1,0,0,1,0,0,0,0],
    "C":   [1,1,0,0,0,1,1,0],
    "E":   [1,0,0,0,0,1,1,0],
    "P":   [1,0,0,0,1,1,0,0],
    "c":   [0,0,1,0,0,1,1,1],
    "o":   [1,0,1,0,0,0,1,1],
    "r":   [1,0,1,0,1,1,1,1],
    "t":   [0,0,0,0,0,1,1,1],
    "off": [1,1,1,1,1,1,1,1],
    "dot": [0,1,1,1,1,1,1,1],
}

# Set list for display position in 8 bin
display_1 = [0,0,0,0,1,0,0,0]
display_2 = [0,0,0,0,0,1,0,0]
display_3 = [0,0,0,0,0,0,1,0]
display_4 = [0,0,0,0,0,0,0,1]

# Pin initialization
GPIO.setup(data_pin, GPIO.OUT)
GPIO.setup(clock_pin, GPIO.OUT)
GPIO.setup(latch_pin, GPIO.OUT)

# Function to send data to 74HC595
def shift_bit(data_pin, clock_pin, latch_pin, sign_1, sign_2, sign_3, sign_4):
    # First set the latch_pin pin low (GPIO.LOW) to prepare the 74HC595
    # to receive data.
    # Display 1
    GPIO.output(latch_pin, 0)
    # First 8 bits = segments to light. Second 8 bits = position
    sign_1 = sign_1 + [0,0,0,0,1,0,0,0]
        # Then use a for loop to transfer each bit of data and position to the chip in sequence
    for i in range(len(sign_1)):
        # Inside the loop, we first set the clock_pin pin low (GPIO.LOW) to get ready to send the next bit.
        GPIO.output(clock_pin, 0)
        # Pass the value bit by bit
        GPIO.output(data_pin, sign_1[i])
        # After that, we set the clock_pin pin to high (GPIO.HIGH) to send the current bit to the chip.
        GPIO.output(clock_pin, 1)
        
    # After the end of the transmission cycle of all bits, we set the clock_pin pin low (GPIO.LOW)
    # and the latch_pin pin high (GPIO.HIGH).
    # This signals to the 74HC595 that all bits have been transferred and it can update its outputs
    # according to the data transferred.
    GPIO.output(clock_pin, 0)
    GPIO.output(latch_pin, 1)

    #Display 2
    GPIO.output(latch_pin, 0)
    sign_2 = sign_2 + [0,0,0,0,0,1,0,0]
    for i in range(len(sign_2)):
        GPIO.output(clock_pin, 0)
        GPIO.output(data_pin, sign_2[i])
        GPIO.output(clock_pin, 1)
    GPIO.output(clock_pin, 0)
    GPIO.output(latch_pin, 1)

    #Display 3
    GPIO.output(latch_pin, 0)
    sign_3 = sign_3 + [0,0,0,0,0,0,1,0]
    for i in range(len(sign_3)):
        GPIO.output(clock_pin, 0)
        GPIO.output(data_pin, sign_3[i])
        GPIO.output(clock_pin, 1)
    GPIO.output(clock_pin, 0)
    GPIO.output(latch_pin, 1)

    #Display 4
    GPIO.output(latch_pin, 0)
    sign_4 = sign_4 + [0,0,0,0,0,0,0,1]
    for i in range(len(sign_4)):
        GPIO.output(clock_pin, 0)
        GPIO.output(data_pin, sign_4[i])
        GPIO.output(clock_pin, 1)
    GPIO.output(clock_pin, 0)
    GPIO.output(latch_pin, 1)

# Function to get time digit by digit
def get_time():
    now = datetime.datetime.now().time()
    hour = now.hour
    minute = now.minute

    # Dividing time into specific numbers
    hour_tens = hour // 10
    hour_ones = hour % 10
    minute_tens = minute // 10
    minute_ones = minute % 10
    # Add dot for second characters
    #hour_ones_dot = [0] + digit[hour_ones][1:8]
    return [hour_tens, hour_ones, minute_tens, minute_ones]

# Script Start

while True:
    try:
        t = get_time()
        shift_bit(data_pin, clock_pin, latch_pin, digit[t[0]], digit[t[1]], digit[t[2]], digit[t[3]])
    except:
        shift_bit(data_pin, clock_pin, latch_pin, digit["off"], digit["off"], digit["off"], digit["off"])
        GPIO.cleanup()