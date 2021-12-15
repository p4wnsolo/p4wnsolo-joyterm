#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014-2020 Richard Hull and contributors
# See LICENSE.rst for details.
# PYTHON_ARGCOMPLETE_OK

"""
Simple println capabilities.
"""

import os
import time
import subprocess
from pathlib import Path
from demo_opts import get_device
from luma.core.virtual import terminal
from PIL import ImageFont

# Init variables
textfile = 'theoutput.txt'
brpath = '/home/pi/p4wnsolo/blueranger.sh'
inputfile = 'thecommand.txt'

# Get input
file1 = open(inputfile, 'r')
userinput = file1.readlines()
userinput = userinput[1]
userinput = userinput.strip('\n')
print('\nCommand: ' + str(userinput) + '\n')

def make_font(name, size):
    font_path = str(Path(__file__).resolve().parent.joinpath('fonts', name))
    return ImageFont.truetype(font_path, size)

print("Displaying output..\n")
# Define output file name variable
outputfilename = textfile

# Open the output file in WRITE mode (for logging)
outputfile = open(outputfilename, "w")

# Define script command to be run, insert the MAC, output to txt log file
prep_cmd = userinput
cmd = prep_cmd + " >> " + outputfilename
print(cmd)

######################## Run the script Subprocess ################################
pro = subprocess.Popen(cmd, stdout=subprocess.PIPE,shell=True, preexec_fn=os.setsid) 

print('\n*****OUTPUT*****:\n')

def main():
    while True:
        for fontname, size in [(None, None), ("tiny.ttf", 6), ("ProggyTiny.ttf", 16), ("creep.bdf", 16), ("miscfs_.ttf", 12), ("FreePixel.ttf", 12), ('ChiKareGo.ttf', 16)]:
            font = make_font(fontname, size) if fontname else None
            term = terminal(device, font)
            term.clear()
            
            with open(textfile) as f:
               for line in f:
                   # For Python3, use print(line)
                   print(line.strip('\n'))
                   term.println(line.strip('\n'))
                   if 'xyz' in line:
                      break
            time.sleep(2)
            exit()

if __name__ == "__main__":
    try:
        device = get_device()
        main()
    except KeyboardInterrupt:
        pass
