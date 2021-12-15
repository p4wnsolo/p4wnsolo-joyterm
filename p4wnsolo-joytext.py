# -*- coding:utf-8 -*-
import SH1106
import time
import config
import traceback
import subprocess
import socket
import fcntl
import struct
import fontawesome as fa
import os
import json
import RPi.GPIO as GPIO

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

#GPIO define
RST_PIN        = 25
CS_PIN         = 8
DC_PIN         = 24

KEY_UP_PIN     = 6 
KEY_DOWN_PIN   = 19
KEY_LEFT_PIN   = 5
KEY_RIGHT_PIN  = 26
KEY_PRESS_PIN  = 13

KEY1_PIN       = 21
KEY2_PIN       = 20
KEY3_PIN       = 16

# Init variables
prefix = './'  # Working folder
#prefix = '/root/BeBoXGui/'  # Kali Linux
mnu_file = prefix + 'themenu.txt'
command_textfile = prefix + 'thecommand.txt'

# 240x240 display with hardware SPI:
disp = SH1106.SH1106()
disp.Init()


with open(command_textfile, 'r') as sf:
    if 1 == 1:
        print('\nSaved SSID was not found in SSIDs file or user selected No - Do not reconnect.  Showing WiFi scan results.\n')

        # Clear display.
        disp.clear()
        # time.sleep(1)
        
        #init GPIO
        # for P4:
        # sudo vi /boot/config.txt
        # gpio=6,19,5,26,13,21,20,16=pu
        GPIO.setmode(GPIO.BCM) 
        GPIO.setup(KEY_UP_PIN,      GPIO.IN, pull_up_down=GPIO.PUD_UP)    # Input with pull-up
        GPIO.setup(KEY_DOWN_PIN,    GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Input with pull-up
        GPIO.setup(KEY_LEFT_PIN,    GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Input with pull-up
        GPIO.setup(KEY_RIGHT_PIN,   GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
        GPIO.setup(KEY_PRESS_PIN,   GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
        GPIO.setup(KEY1_PIN,        GPIO.IN, pull_up_down=GPIO.PUD_UP)      # Input with pull-up
        GPIO.setup(KEY2_PIN,        GPIO.IN, pull_up_down=GPIO.PUD_UP)      # Input with pull-up
        GPIO.setup(KEY3_PIN,        GPIO.IN, pull_up_down=GPIO.PUD_UP)      # Input with pull-up

        # Create blank image for drawing.
        # Make sure to create image with mode '1' for 1-bit color.
        image = Image.new('1', (disp.width, disp.height), "WHITE")

        # Get drawing object to draw on image.
        draw = ImageDraw.Draw(image)

        # Set font.  Default myfont = './fonts/DroidSansMono.ttf'

        myfont = prefix + 'fonts/DroidSansMono.ttf'  # Editor's number 1 pick
        iconfont = prefix + 'fonts/fontawesome-webfont.ttf'  # FontAwesome   #fontawesome-webfont.ttf

        font12 = ImageFont.truetype(myfont, 12)    
        font16 = ImageFont.truetype(myfont, 16)    
        iconsize12 = ImageFont.truetype(iconfont, 12)    
        iconsize13 = ImageFont.truetype(iconfont, 13)    
        iconsize14 = ImageFont.truetype(iconfont, 14)    
        iconsize15 = ImageFont.truetype(iconfont, 15)    
        iconsize16 = ImageFont.truetype(iconfont, 16)    
        iconsize17 = ImageFont.truetype(iconfont, 17)    
        iconsize18 = ImageFont.truetype(iconfont, 18)    

        # Init some variables
        thestring = ''
        selection = 0
        charset_sel = 0  # 0 = 0-9,  1 = A-Z,  2 = special, 3 = a-z
        charset_sel_end = 3 # This is the number of the last charset  (# charsets minus 1)
        restrict_to_this_charset = 0  # Initialize restrict to this charset toggle
        no_special_characters = 0  # Init the no_special_characters variable

        # Set x,y for top left corner of selection box
        selection_y1 = 28
        selection_y2 = 45

        # Set the default mode
        mode = "general"  # Set the default mode

        # Set which character set(s) should be used  # Default (General mode) is:  charset_az_upper_enabled = 1, all others 0
        charset_az_upper_enabled = 0  # General Mode:  az_upper_enabled = 1, all others 0
        charset_az_lower_enabled = 0 # Not yet implemented
        charset_09_enabled = 0  # Phone Mode:  09_enabled = 1, all others 0
        charset_hx_enabled = 0  # MAC Address Mode:  hx_enabled = 1, all others 0 # This may be unneeded
        charset_em_enabled = 0  # Nix this - just use General layout for email?
        charset_sp_enabled = 0  # Special characters
        charset_ip_enabled = 0  # IP Address characters

        # Set the MODE (if different than default, which is General mode)
        #mode = "phone"  # Uncomment to enable
        #mode = "mac"  # Uncomment to enable
        #mode = "plate"  # Uncomment to enable
        #mode = "general"  # Enabled by default
        #mode = "ip"  # Uncomment to enable


        # General mode (enabled by default)
        if mode == "general":
            charset_az_upper_enabled = 1  # General mode: az_upper_enabled = 1, all others 0
            restrict_to_this_charset = 0

        # Phone mode
        if mode == "phone":
            charset_09_enabled = 1  # Phone Mode:  09_enabled = 1, all others 0
            restrict_to_this_charset = 1

        # MAC mode (aka Hex mode)
        if mode == "mac":
            charset_hx_enabled = 1  # Hex Mode:  hx_enabled = 1, all others 0
            restrict_to_this_charset = 1

        # Plate mode (aka License plate mode)
        if mode == "plate":
            charset_az_upper_enabled = 1
            no_special_characters = 1

        # IP address mode 
        if mode == "ip":
            charset_ip_enabled = 1
            #no_special_characters = 1
            restrict_to_this_charset = 1

        # Init num_elements 
        num_elements = 0

        # A-Z 
        if charset_az_upper_enabled == 1 or charset_az_lower_enabled:
            num_elements = num_elements + 27
        # 0-9
        if charset_09_enabled == 1:
            num_elements = num_elements + 11
        # Hexadecimal
        if charset_hx_enabled == 1:
            num_elements = num_elements + 16  # If colon is needed, change this to 17 from 16
        # Email
        if charset_em_enabled == 1:
            num_elements = num_elements + 2
        # Special characters
        if charset_sp_enabled == 1:
            num_elements = num_elements + 22
        # IP address characters
        if charset_ip_enabled == 1:
            num_elements = num_elements + 11  # If colon is needed, change this to 12 from 11

        # Init a variable and set the last element
        num_first_element = 0
        num_last_element = num_elements - 1

        # Start the main loop
        while 1:

            # with canvas(device) as draw:
            if GPIO.input(KEY_UP_PIN): # UP button is released
                draw.polygon([(38, 5), (48, 0), (58, 5)], outline=255, fill=0)  #Up
            else: # UP button is pressed:
                # Toggle the changing of selection box's "y coordinates" by uncommenting the two lines below
                #selection_y1 = ((selection * 14) + 11)
                #selection_y2 = ((selection * 14) + 23)
                draw.polygon([(38, 5), (48, 0), (58, 5)], outline=0, fill=1)  #Up filled
                print("Up")
                
            if GPIO.input(KEY_LEFT_PIN): # LEFT button is released
                draw.polygon([(0, 30), (6, 21), (6, 41)], outline=255, fill=0)  #left
            else: # LEFT button is pressed:
                # Decrement the selection counter if user hasn't reached the 1st element
                if selection > num_first_element:
                    selection = selection - 1
                # If the user DID reach the first element, set the selection to the last element instead of decrementing
                elif selection == num_first_element:
                    selection = num_last_element

                draw.polygon([(0, 30), (6, 21), (6, 41)], outline=0, fill=1)  #left filled
                print("left")
                
            if GPIO.input(KEY_RIGHT_PIN): # button is released
                draw.polygon([(95, 30), (89, 21), (89, 41)], outline=255, fill=0) #right
            else: # button is pressed:
                # Increment the Selection counter if the user hasn't reached the last item yet
                if selection < num_last_element:
                    selection = selection + 1
                elif selection == num_last_element:
                    selection = num_first_element

                draw.polygon([(95, 30), (89, 21), (89, 41)], outline=0, fill=1) #right filled
                print("right")
                
            if GPIO.input(KEY_DOWN_PIN): # DOWN button is released
                #if selection == 2:
                draw.polygon([(48, 60), (58, 54), (38, 54)], outline=255, fill=0) #down
            else: # DOWN button is pressed:
                draw.polygon([(48, 60), (58, 54), (38, 54)], outline=0, fill=1) #down filled
                print("down")
                print(selection)

            if GPIO.input(KEY_PRESS_PIN): # CENTER button is released        

                # Set y-coordinates of selection Box according to the value of "selection" variable
                # Uncomment the lines below to make it so the selection box moves up and down (for MENU)
                #selection_y1 = ((selection * 14) + 7)
                #selection_y2 = ((selection * 14) + 19)

                # Read menu items from txt file
                with open(mnu_file, 'r') as f:
                    line7 = f.readlines()[-4]
                    print(line7)
                with open(mnu_file, 'r') as f:
                    line8 = f.readlines()[-3]
                    print(line8)
                with open(mnu_file, 'r') as f:
                    line9 = f.readlines()[-2]
                    print(line9)
                with open(mnu_file, 'r') as f:
                    line10 = f.readlines()[-1]
                    print(line10)

                # Set experimental variable for test
                # Set font-awesome icon
                faicon4 = fa.icons['wifi'] + fa.icons['power-off'] + fa.icons['bluetooth'] + fa.icons['toggle-on'] + fa.icons['toggle-off'] + fa.icons['plug'] 

                # Draw the text!
                draw.text((2, 43), faicon4, font = iconsize14, fill = 0)

            
                # Set OLED text line variables
                oled_line_1 = line7
                oled_line_2 = ''
                oled_line_3 = ''
                oled_line_4 = ''#faicon4 #line7
                
                # Get length of input string
                stringlength = len(thestring)

                # Set letter-selection-box x1 and x2 coordinates
                selection_x1 = ((stringlength * 7) + 1)
                selection_x2 = ((stringlength * 7) + 12)

                # Temporarily redefine the text lines for alphabet input
                oled_line_3 = str(selection)
                if charset_az_upper_enabled == 1 or charset_az_lower_enabled:
                    if selection == 0:
                        ltr = 'a'
                    elif selection == 1:
                        ltr = 'b'
                    elif selection == 2:
                        ltr = 'c'
                    elif selection == 3:
                        ltr = 'd'
                    elif selection == 4:
                        ltr = 'e'
                    elif selection == 5:
                        ltr = 'f'
                    elif selection == 6:
                        ltr = 'g'
                    elif selection == 7:
                        ltr = 'h'
                    elif selection == 8:
                        ltr = 'i'
                    elif selection == 9:
                        ltr = 'j'
                    elif selection == 10:
                        ltr = 'k'
                    elif selection == 11:
                        ltr = 'l'
                    elif selection == 12:
                        ltr = 'm'
                    elif selection == 13:
                        ltr = 'n'
                    elif selection == 14:
                        ltr = 'o'
                    elif selection == 15:
                        ltr = 'p'
                    elif selection == 16:
                        ltr = 'q'
                    elif selection == 17:
                        ltr = 'r'
                    elif selection == 18:
                        ltr = 's'
                    elif selection == 19:
                        ltr = 't'
                    elif selection == 20:
                        ltr = 'u'
                    elif selection == 21:
                        ltr = 'v'
                    elif selection == 22:
                        ltr = 'w'
                    elif selection == 23:
                        ltr = 'x'
                    elif selection == 24:
                        ltr = 'y'
                    elif selection == 25:
                        ltr = 'z'
                    elif selection == 26:
                        ltr = ' '
                    if charset_az_lower_enabled == 1:
                        ltr = str(ltr.upper())

                # Special characters
                if charset_sp_enabled == 1:
                    if selection == 0:
                        ltr = '.'
                    elif selection == 1:
                        ltr = '@'
                    elif selection == 2:
                        ltr = '+'
                    elif selection == 3:
                        ltr = ':'
                    elif selection == 4:
                        ltr = '/'
                    elif selection == 5:
                        ltr = '\\'
                    elif selection == 6:
                        ltr = '!'
                    elif selection == 7:
                        ltr = '?'
                    elif selection == 8:
                        ltr = '^'
                    elif selection == 9:
                        ltr = '&'
                    elif selection == 10:
                        ltr = '*'
                    elif selection == 11:
                        ltr = '('
                    elif selection == 12:
                        ltr = ')'
                    elif selection == 13:
                        ltr = '-'
                    elif selection == 14:
                        ltr = '_'
                    elif selection == 15:
                        ltr = '='
                    elif selection == 16:
                        ltr = '$'
                    elif selection == 17:
                        ltr = '%'
                    elif selection == 18:
                        ltr = ','
                    elif selection == 19:
                        ltr = ';'
                    elif selection == 20:
                        ltr = '|'
                    elif selection == 21:
                        ltr = ' '

                # 0-9
                if charset_09_enabled == 1:
                    if selection < 10:
                        ltr = str(selection)
                    elif selection > 9:
                        if selection == 10:
                            ltr = '.'
                        if selection == 11:
                            ltr = ' '

                # HEX
                if charset_hx_enabled == 1:
                    if selection < 10:
                        ltr = str(selection)
                    elif selection > 9:
                        if selection == 10:
                            ltr = 'A'
                        elif selection == 11:
                            ltr = 'B'
                        elif selection == 12:
                            ltr = 'C'
                        elif selection == 13:
                            ltr = 'D'
                        elif selection == 14:
                            ltr = 'E'
                        elif selection == 15:
                            ltr = 'F'
                        elif selection == 16:
                            ltr = ':'
                    # Auto add a colon (:) after every 2 characters
                    if stringlength == 1 or stringlength == 4 or stringlength == 7 or stringlength == 10:   # I canceled implementing auto-advance to next IP address field
                        ltr = ltr + ':'       # and auto-adding ':'

                # IP address
                if charset_ip_enabled == 1:
                    if selection < 10:
                        ltr = str(selection)
                        #if stringlength == 2:   # I canceled implementing auto-advance to next IP address field
                        #    ltr = ltr + '.'       # and auto-adding '.'
                    elif selection > 9:
                        if selection == 10:
                            ltr = '.'
                        elif selection == 11:
                            ltr = ':'

                # Email
                if charset_em_enabled == 1:
                    if selection == 0:
                        ltr = '@'
                    elif selection == 1:
                        ltr = '.'

                draw.rectangle((0, 0,127,63), outline=0, fill=1) # Rectangle around entire area

                # Draw the selection Box
                draw.rectangle((selection_x1, selection_y1,selection_x2,selection_y2), outline=0, fill=1) #center filled
                
                # Print the current selection to the console
                print("Current selection: " + str(selection))
                print("Current letter: " + str(ltr))
                print("Current charset selection number: " + str(charset_sel))
                print("Current String: " + thestring)
                print("Length of string: " + str(stringlength))
                print("Selection x1 coordinate: " + str(selection_x1))
                print("Selection x2 coordinate: " + str(selection_x2))
                print("Selection y1 coordinate: " + str(selection_y1))
                print("Selection y2 coordinate: " + str(selection_y2))
                # Draw the text!
                oled_line_3 = thestring + ltr
                draw.text((2, 1), oled_line_1, font = font12, fill = 0)
                draw.text((2, 15), oled_line_2, font = font12, fill = 0)
                draw.text((2, 29), oled_line_3, font = font12, fill = 0)
                draw.text((2, 46), oled_line_4, font = iconsize16, fill = 0)
                #draw.text((9, 34), oled_line_3, font = font12, fill = 0)

            else: # CENTER button is pressed:
                thestring = thestring + ltr

                stringlength = len(thestring)

                # Draw the text!
                draw.text((9, 6), oled_line_1, font = font12, fill = 0)
                draw.text((9, 20), oled_line_2, font = font12, fill = 0)
                draw.text((9, 34), thestring + ltr, font = font12, fill = 0)
                print("center")

                draw.text((9, 6), oled_line_1, font = iconsize16, fill = 0)
                # Create blank image for drawing.
                # Make sure to create image with mode '1' for 1-bit color.
                image = Image.new('1', (disp.width, disp.height), "WHITE")

                # Get drawing object to draw on image.
                draw = ImageDraw.Draw(image)
                
            if GPIO.input(KEY1_PIN): # KEY1 button is released
                draw.ellipse((106,0,126,21), outline=0, fill=1) #A button

                # Set font-awesome icon
                faicon1 = fa.icons['keyboard']

                # Draw the text!
                draw.text((109, 3), faicon1, font = iconsize14, fill = 0)

            # Switch charsets when KEY1 is pressed
            else: # KEY 1 button is pressed:

                # Set font-awesome icon
                faicon1 = fa.icons['keyboard']

                # Draw the text!
                draw.text((109, 3), faicon1, font = iconsize14, fill = 0)

                # Check if a unique mode isn't enabled (mac, license plate, IP address) to disable charset switch button for unique modes
                if restrict_to_this_charset < 1:
                    # If charset selection is 1 (A-Z) then turn on a-z, turn off other charsets, increment the charset selection, set # elements in charset
                    if charset_sel == 0:  # A-Z charset
                        # Toggle charset
                        charset_09_enabled = 1
                        # Toggle charset
                        charset_az_upper_enabled = 0
                        # NEW Toggle charset
                        charset_sel = charset_sel + 1
                        # Update num of elements to new charset
                        num_elements = 12
                        # Re-set the num of the FIRST element in the set
                        num_first_element = 0
                        # Re-set the num of the last element in the set
                        num_last_element = num_elements - 1
                    elif charset_sel == 1:  # 0-9 charset
                        # Toggle charset
                        charset_09_enabled = 0
                        # Increment selected charset if special characters are allowed
                        if no_special_characters == 1:
                            charset_sel = 0
                            # Toggle charset
                            charset_az_upper_enabled = 1
                            # Update num of elements to new charset
                            num_elements = 27
                            # Re-set the num of the FIRST element in the set
                            num_first_element = 0
                            # Re-set the num of the last element in the set
                            num_last_element = num_elements - 1
                        elif no_special_characters < 1:
                            # Toggle charset
                            charset_sp_enabled = 1
                            charset_sel = charset_sel + 1
                            # Update num of elements to new charset
                            num_elements = 20
                        # Re-set the num of the FIRST element in the set
                        num_first_element = 0
                        # Re-set the num of the LAST element in the set
                        num_last_element = num_elements - 1
                    # If the selected charset is A-Z, then disable A-Z and enabled 0-9
                    # If the selected charset is 0-9, then disable 0-9 and enable Special characters
                    elif charset_sel == 2:  # Special charset
                        # Toggle charset
                        charset_sp_enabled = 0
                        # Toggle charset
                        charset_az_lower_enabled = 1
                        # NEW Toggle charset
                        if charset_sel < charset_sel_end:
                            charset_sel = charset_sel + 1
                        elif charset_sel == charset_sel_end:
                            charset_sel = charset_sel + 1
                        # Update num of elements to new charset
                        num_elements = 27
                        # Re-set the num of the FIRST element in the set
                        num_first_element = 0
                        # Re-set the num of the last element in the set
                        num_last_element = num_elements - 1
                    elif charset_sel == 3:  # Special charset
                        # Toggle charset
                        charset_az_upper_enabled = 1
                        # Toggle charset
                        charset_az_lower_enabled = 0
                        # NEW Toggle charset
                        charset_sel = 0
                        # Update num of elements to new charset
                        num_elements = 27
                        # Re-set the num of the FIRST element in the set
                        num_first_element = 0
                        # Re-set the num of the last element in the set
                        num_last_element = num_elements - 1

                ##### Re-set the current selection to 0
                selection = 0
                
                draw.ellipse((106,0,126,21), outline=255, fill=0) #A button filled
                print("KEY1")
                # Create blank image for drawing.
                # Make sure to create image with mode '1' for 1-bit color.
                image = Image.new('1', (disp.width, disp.height), "WHITE")

                # Get drawing object to draw on image.
                draw = ImageDraw.Draw(image)
                
                
            if GPIO.input(KEY2_PIN): # button is released
                draw.ellipse((106,22,126,42), outline=0, fill=1) #A buttton
                # Set font-awesome icon
                faicon2 = fa.icons['times-circle']

                # Draw the text!
                draw.text((110, 24), faicon2, font = iconsize16, fill = 0)

            else: # button is pressed:
                draw.ellipse((101,22,121,42), outline=255, fill=0) #A button filled

                # Set font-awesome icon
                faicon2 = fa.icons['times-circle']

                # Draw the text!
                draw.text((105, 24), faicon2, font = iconsize16, fill = 1)

                # Remove the last character from the string being entered
                thestring = thestring[:-1]

                print("KEY3")


            if GPIO.input(KEY3_PIN): # button is released
                draw.ellipse((106,42,126,62), outline=0, fill=1) #B button]
                
                # Set font-awesome icon
                faicon3 = fa.icons['chevron-right']

                # Draw the text!
                draw.text((112, 45), faicon3, font = iconsize16, fill = 0)

            else: # button is pressed:
                try:
                    disp = SH1106.SH1106()
                    disp.Init()
                    disp.clear()
                    image1 = Image.new('1', (disp.width, disp.height), "WHITE")
                    draw = ImageDraw.Draw(image1)
                    font16 = ImageFont.truetype(prefix + 'fonts/Prototype.ttf', 16)
                    font13 = ImageFont.truetype(prefix + 'fonts/Prototype.ttf', 13)
                    draw.line([(0,0),(127,0)], fill = 0)
                    draw.line([(0,0),(0,63)], fill = 0)
                    draw.line([(0,63),(127,63)], fill = 0)
                    draw.line([(127,0),(127,63)], fill = 0)
                    draw.text((0,8), '      Running', font = font16, fill = 0)
                    disp.ShowImage(disp.getbuffer(image1))
                except IOError as e:
                    print(e)
                except KeyboardInterrupt:    
                    print("ctrl + c:")
                    epdconfig.module_exit()
                    exit()


                draw.ellipse((106,42,126,62), outline=255, fill=0) #B button filled
                
                # Set font-awesome icon
                faicon3 = fa.icons['check']

                # Draw the text!
                draw.text((5, 28), faicon3, font = iconsize16, outline=255, fill = 0)

                print("KEY3")

                # Open the text file
                open(command_textfile, 'w').close()  # Erase it with .close
                f = open(command_textfile, "a")   # Open the file for Append mode
                f.write('\n')
                f.write(thestring + '\n')


                # Draw the text!
                draw.text((0,28), '        Started', font = font13, fill = 0)

                # Create blank image for drawing.
                # Make sure to create image with mode '1' for 1-bit color.
                image = Image.new('1', (disp.width, disp.height), "WHITE")

                # Get drawing object to draw on image.
                draw = ImageDraw.Draw(image)
                
                # Show the new image
                disp.ShowImage(disp.getbuffer(image1))

                # Sleep
                print("\nSleeping a few seconds..\n")
                
                # Exit the program
                exit()

            disp.ShowImage(disp.getbuffer(image))
        
    # except:
        # print("except")
    # GPIO.cleanup()
