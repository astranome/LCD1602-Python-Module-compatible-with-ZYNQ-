#!/usr/bin/python
#--------------------------------------
#  Copyright (c) 2024 Andrew Kobelev
#  mt16s2r.py
#  Test Script
#  Use HD44780-compatible 16x2 LCD module via gpiod 
#  Display manufacturer : MELT company
#  http://www.melt.aha.ru/en/
#  made based on the code
#  https://www.sunfounder.com/
#  and https://pypi.org/project/gpiod/
#--------------------------------------
 
# The wiring for the LCD is as follows:
# 15: LCD Backlight +5V**
# 16: LCD Backlight GND
# 1 : GND
# 2 : 5V
# 3 : Contrast (0-5V)*
# 4 : RS (Register Select)
# 5 : R/W (Read Write)       - GROUND THIS PIN
# 6 : Enable or Strobe
# 7 : Data Bit 0             - NOT USED
# 8 : Data Bit 1             - NOT USED
# 9 : Data Bit 2             - NOT USED
# 10: Data Bit 3             - NOT USED
# 11: Data Bit 4
# 12: Data Bit 5
# 13: Data Bit 6
# 14: Data Bit 7

import gpiod
import time
from gpiod.line import Direction, Value 
import time
# You can get the Pin names by `gpioinfo`
# Define GPIO to LCD mapping
LCD_RS = "P9"
LCD_E  = "P7"
LCD_D4 = "P1"
LCD_D5 = "P3"
LCD_D6 = "P5"
LCD_D7 = "P15"
LED_ON = "P0"
 
# Define some device constants
LCD_WIDTH = 16    # Maximum characters per line
LCD_CHR = True
LCD_CMD = False
 
LCD_LINE_1 = 0x00 # LCD RAM address for the 1st line
LCD_LINE_2 = 0x10 # LCD RAM address for the 2nd line

 
# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005
# You can get the chip name by `gpiodetect`
def output(line_offset, val, chip_path="/dev/gpiochip0"):
    value_str = {Value.ACTIVE: "Active", Value.INACTIVE: "Inactive"}
    if val == True:
        value = Value.ACTIVE
    else:
        value = Value.INACTIVE

    with gpiod.request_lines(
        chip_path,
        consumer="Astra-LAB",
        config={
            line_offset: gpiod.LineSettings(
                direction=Direction.OUTPUT, output_value= value
            )
        },
    ) as request:
        
        request.set_value(line_offset, value)

def main():
  # Main program block
    lcd_init()

  # Toggle backlight on-off-on
    lcd_backlight(True)
    time.sleep(0.5)
    lcd_backlight(False)
    time.sleep(0.5)
    lcd_backlight(True)
    time.sleep(0.5)
    
    while True:
        # the loop with debug purpose
     # Send some centred test
        lcd_init()
        lcd_byte(0x80,LCD_CMD) # 000110 Cursor move to 1st line 
        lcd_string("===Astra LAB===*",LCD_LINE_1,1)
        lcd_byte(0xC0,LCD_CMD) #  Curs 2 second line
        lcd_string("*-MT-16SR2-4 Bit*",LCD_LINE_2,2)
        
        print("Send 4 str") # debug message
        time.sleep(3) # 3 second delay

def lcd_init():
  # Initialise display
    time.sleep(0.02)
    lcd_toggle_enable()
    lcd_byte(0x03,LCD_CMD) # 000011 Initialise
    time.sleep(0.001)
    lcd_byte(0x03,LCD_CMD) # 000011 Initialise
    time.sleep(0.001)
    lcd_byte(0x03,LCD_CMD) # 000011 Initialise
    time.sleep(0.001)

    lcd_byte(0x02,LCD_CMD) # 000010 Initialise
    time.sleep(0.001)
    
    lcd_byte(0x2A,LCD_CMD) # 000010 Initialise 02 RIGHT MODE
    lcd_byte(0x0C,LCD_CMD) # 001000 Initialise ON
    lcd_byte(0x01,LCD_CMD) # 000001 Clear display
    lcd_byte(0x06,LCD_CMD) # 000001 MODE display
    lcd_byte(0x00,LCD_CMD) # 000000 Initialise
    lcd_byte(0x06,LCD_CMD) # 000110 Cursor move direction
    print("init ----Done") # debug message
    time.sleep(E_DELAY)
    print("init Done*****************************************")
def lcd_byte(bits, mode):
  # Send byte to data pins
  # bits = data
  # mode = True  for character
  #        False for command
 
  output(LCD_RS, mode) # RS
 
  # High bits
  output(LCD_D4, False)
  output(LCD_D5, False)
  output(LCD_D6, False)
  output(LCD_D7, False)
  if bits&0x10==0x10:
   output(LCD_D4, True)
  if bits&0x20==0x20:
    output(LCD_D5, True)
  if bits&0x40==0x40:
    output(LCD_D6, True)
  if bits&0x80==0x80:
    output(LCD_D7, True)
  #print("H-Done")
  # Toggle 'Enable' pin
  lcd_toggle_enable()
 
  # Low bits
  output(LCD_D4, False)
  output(LCD_D5, False)
  output(LCD_D6, False)
  output(LCD_D7, False)
  if bits&0x01==0x01:
    output(LCD_D4, True)
  if bits&0x02==0x02:
    output(LCD_D5, True)
  if bits&0x04==0x04:
    output(LCD_D6, True)
  if bits&0x08==0x08:
    output(LCD_D7, True)
  # print("Low and High Bits puts to LCD")
  # Toggle 'Enable' pin
  lcd_toggle_enable()
 
def lcd_toggle_enable():
  # Toggle enable
  time.sleep(E_DELAY)
  output(LCD_E, True)
  time.sleep(E_PULSE)
  output(LCD_E, False)
  time.sleep(E_DELAY)
  # print("STROBE")
def lcd_string(message,line,style):
  # Send string to display
  # style=1 Left justified
  # style=2 Centred
  # style=3 Right justified
 
  if style==1:
    message = message.ljust(LCD_WIDTH," ")
  elif style==2:
    message = message.center(LCD_WIDTH," ")
  elif style==3:
    message = message.rjust(LCD_WIDTH," ")
 
  lcd_byte(line, LCD_CMD)
 
  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)
 
def lcd_backlight(flag):
  # Toggle backlight on-off-on
  output(LED_ON, flag)
 
if __name__ == '__main__':
 
  try:
    main()
  except KeyboardInterrupt:
    pass
