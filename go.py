#!/usr/bin/python
# -*- coding:utf-8 -*-

import subprocess

from pathlib import Path
home = str(Path.home())  # Get home folder (makes it cross-platform)

print('\nHome: ' + home + '\n')

### Script A
a1 = '/usr/bin/python3'
a2 = home + '/p4wnsolo/p4wnsolo-joyterm/p4wnsolo-joytext.py'
subprocess.call([a1, a2])  # Run script

### Script B
b1 = '/usr/bin/python3'
b2 = home + '/p4wnsolo/p4wnsolo-joyterm/p4wnsolo-terminal.py'
b3 = '-i'
b4 = 'spi'
b5 = '--display'
b6 = 'sh1106'
b7 = '--rotate'
b8 = '2'
subprocess.call([b1, b2, b3, b4, b5, b6, b7, b8])  # Run script
