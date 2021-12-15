#!/usr/bin/python
# -*- coding:utf-8 -*-

import subprocess

a1 = '/usr/bin/python3'
a2 = '/home/pi/BeBoXGui/p4wnsolo-joyterm/p4wnsolo-joytext.py'

subprocess.call([a1, a2])

b1 = '/usr/bin/python3'
b2 = '/home/pi/BeBoXGui/p4wnsolo-joyterm/p4wnsolo-terminal.py'
b3 = '-i'
b4 = 'spi'
b5 = '--display'
b6 = 'sh1106'
b7 = '--rotate'
b8 = '2'

subprocess.call([b1, b2, b3, b4, b5, b6, b7, b8])
