#!/usr/bin/python
# -*- coding:utf-8 -*-

import subprocess
import pathlib
from pathlib import Path

prefix = str(pathlib.Path(__file__).parent.resolve()) + '/'
home = str(Path.home())  # Get home folder (makes it cross-platform)

print('\nHome: ' + home + '\n')
print('This folder: ' + prefix + '\n')

### Script A
a1 = '/usr/bin/python3'
a2 = prefix + 'p4wnsolo-joytext.py'
subprocess.call([a1, a2])  # Run script

### Script B
b1 = '/usr/bin/python3'
b2 = prefix + 'p4wnsolo-terminal.py'
b3 = '-i'
b4 = 'spi'
b5 = '--display'
b6 = 'sh1106'
b7 = '--rotate'
b8 = '2'
subprocess.call([b1, b2, b3, b4, b5, b6, b7, b8])  # Run script
