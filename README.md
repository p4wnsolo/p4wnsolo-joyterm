# 🕹️ p4wnsolo-joyterm
* Gets text input from OLED Joystick
* Runs the command you typed
* Displays output on OLED Screen 
*(Great for P4wnP1 - even better on Raspberry Pi Zero 2)*

<img src="/images/p4wnsolo-joyterm-joytext.jpg">
<img src="/images/p4wnsolo-joyterm-output.jpg">

This is a small collection of a few scripts I put together to enable Terminal functionality on Raspberry Pi with OLED screen (especially P4wnP1).

It is assumed that you already got your OLED screen working *before* trying p4wnsolo-joyterm (see <a href="https://github.com/pimoroni/sh1106-python">SH1106 on Github</a>).

## 💡 Notes 
#### 🐇 Performance (Pi0W vs Pi02)
Everything about this project runs *way* faster and more smoothly on Raspberry Pi Zero 2.

But until nexmon is released for RPi02W, we're stuck with slower performance (if you're dead set on using P4wnP1 as your OS - and if so, I don't blame you one bit).  

It's entirely possible that the code in this repo is so sloppy that it's causing the joystick-press performance to suffer on RPiZeroW.  But like I said - it runs perfectly (and FAST) on Raspberry Pi Zero 2 (see <a href="https://twitter.com/p4wnsolo/status/1470547554085474307">Demo video clip on Twitter</a> 0m19s)

So for now, here's a Demo / pre-release to get you entering commands using that little Joystick on your P4wnP1.

#### ⚙️ Functionality
Currently, p4wnsolo-joyterm just runs a "one shot".
It runs a command and displays the output - but does not wait for more output (yet).
For example, Wifite runs just fine - but p4wnsolo-joyterm Exits when Wifite asks for input.
I'm working on making the Terminal persist while the program continues running, so you can continue adding input after the program starts.
Stay tuned for this update, which should be coming soon.

## 📝 Requirements:
### Hardware:
* Raspberry Pi (any model should work - tested successfully on RPi0W [OS: P4wnP1_ALOA] and RPi02W [OS:  RaspberryPi OS]
* SH1106 OLED Screen (1.3" by Waveshare)
### Software:
* Linux (so far tested on P4wnP1 ALOA [Kali] and Raspberry Pi OS [Debian])
* <a href="https://pypi.org/project/luma.core/">luma and luma.oled</a>
* <a href="https://numpy.org/install/">numpy</a>
* SPI must be enabled (I use Method 3 in <a href="https://www.raspberrypi-spy.co.uk/2014/08/enabling-the-spi-interface-on-the-raspberry-pi/">this RaspberryPi-spy article</a>)

##### How to Install numpy, Luma, Luma.OLED
Tip #1:  Luma.OLED takes ~10 mins to install on RPi 0 W, while numpy takes ~20 mins.
<br />
<code>sudo pip3 install luma luma.oled numpy -y</code>
<br />
Tip #2:  If you see a "Pillow" / "jpeg" error while installing Luma, don't worry.  The p4wnsolo-joyterm script runs fine even with the error.  If you'd like, you can <a href="https://pypi.org/project/Pillow/">manually install Pillow</a> to make sure that part's good.

## 🔨 Install p4wnsolo-joyterm:
<code>cd ~</code>
<br />
<code>git clone https://github.com/p4wnsolo/p4wnsolo-joyterm.git</code>
<br />
<code>cd p4wnsolo-joyterm</code>
<br />
<code>sudo python3 go.py</code>
<br />

## ▶️ Usage:
1) Use the LEFT and RIGHT buttons on the OLED Joystick to switch characters 
2) Press the CENTER Joystick button to add the current character to the Command Line
3) If you made a mistake, press KEY2 ("X") for Backspace
4) To switch KEYBOARD Layout, press KEY1.  For example, the default keyboard layout is "a-z" (lowercase).
5) Launch the command:  press KEY3 (">")
6) View the command output on the OLED screen

## 💡 Tips:
- The SPACE character (" ") exists in at least two character sets:  "a-z" and "A-Z" (both uppercase and lowercase alphabet character sets have the SPACE character *after* the "Z" character or before the "A" character).
- The character set repeats (or "cycles") when the last character in the set is reached.  So you can just keep scrolling through characters (ex:  If you're on the A character, press Left to go to Z from A, or press Right to go from A to B).

There are four (4) character sets:
- a-z (lowercase) (default)
- 0-9
- special characters
- A-Z (uppercase)

## 💻 Compatibility & Platforms
For developing the script, I actually used a RaspberryPi Zero 2.  
To finish developing the script (make it cross-compatible), I ran it several times on Raspberry Pi Zero W running P4wnP1 ALOA latest.

Testing DONE on Pi Zero W (I ran the scripts on my RPi0W P4wnP1 and changed the code to be cross-platform).

To make the scripts compatible across Kali & Raspberry Pi, I used <a href="https://stackoverflow.com/questions/4028904/what-is-the-correct-cross-platform-way-to-get-the-home-directory-in-python">this code snippet from StackExchange</a>.

## 📁 Files included:
The following list of files are required to run p4wnsolo-joyterm:
##### go.py – Adapted from a code snippet found somewhere
* Launches the scripts that do the actual work:
##### p4wnsolo-joytext.py – Adapted from key_demo.py in SH1106 demo files (but by now it’s its own beast, pretty much)
* Displays the “Enter Command” screen and takes text input using Joystick & buttons on OLED screen
##### p4wnsolo-terminal.py – Adapted from terminal.py in luma.examples
* Runs the command
Prints the output onto the OLED screen

## 💬 Explanation of Scripts in p4wnsolo-joyterm

### What is <code>go.py</code>?
* Launches the “p4wnsolo-joytext.py” script to get text input from joystick and buttons on OLED screen
* Then runs the “p4wnsolo-terminal.py” script to execute the text input (command)

### What is <code>p4wnsolo-joytext.py</code>?

This script displays an “Enter command” screen on the SH1106 OLED display.

Then it waits for the user to press the joystick to change characters (using the Left and Right joystick buttons).

Pressing the “Center” joystick button adds the current character to the line.

KEY1 (font-awesome keyboard icon) switches keyboard layouts:

[0] The default layout is uppercase alphabet (A-Z)
[1] Next is 0-9
[2] Then the special characters (./!@#$%^&* etc)
The SPACE character is currently located in this character set
[3] Finally, we have lowercase alphabet (a-z)
KEY2 (“X”) is the backspace key.
KEY3 (“>”) is the GO button.

##### After you press the GO button:
The joyterm script writes the text you entered into a text file called thecommand.txt.
Last but not least, joyterm shows text to indicate that it's actually running the Command you entered ("Running.. Started").


### What is <code>p4wnsolo-terminal.py</code>?
The terminal.py script is an adaptation of the terminal.py script found in luma.examples repo.
The terminal.py from luma.examples utilizes a LOOP to display “lines” of text on the OLED screen.
But the text it displays is static – it’s generated by simple code (resulting in “Line 1, Line 2, Line 3..”).
So I simply replaced that part of the code to display lines of text from a TEXT FILE.  This was way more interesting than just displaying lines being generated by code.
Now that we got the (excellent) terminal.py (from luma.examples) script to display dynamic content, we’re ready to take the command input from the user and send it to terminal.py.


## 🤖 Entering Commands & text using joystick on OLED screen
Just enter any command you normally would on the Linux command line.
Here are some nice, short, sweet commands if you're out of ideas:
* ls
* iwconfig
* who
* whoami

Or be bold, install Wifite, and try "sudo wifite".


## ✅ The Docket
### To Do
Eventually I'll add these features:
* Run previous command(s) (like pressing the "Up" arrow key in Linux CLI)
* Make some aliases to speed up entry of common commands
* Move command-entry area to very bottom of screen
* (Priority #1) Have the script continue to read lines of text even after the last line was read (until the “X” key is pressed)
* (Priority #2) Have the command-entry area re-appear after no new lines in text file have been read for 2 or 3 seconds
The purpose of this is to enable the user to input more text when a program pauses and asks for user input (such as Wifite and many other hacking programs for Linux)
* Optional cool add-on:  Show a countdown / progress bar/line that fills from top of screen to bottom, to meet the command-entry area when it appears after X seconds of no more text output
* Add a few useful aliases
### Done 
Add space character (” “) between A and Z in A-Z uppercase AND lowercase charsets
Add space character to 0-9 charset

## 👢 Run on Boot
To run this script on boot, just follow the steps below to add p4wnsolo-joyterm to Crontab as a new entry.
#### How to Add p4wnsolo-joyterm to Crontab
* Enter "crontab -e" on command line
* Paste the code below in the first empty line:
<code>@reboot cd /home/pi/BeBoXGui/ && /usr/bin/python3 /home/pi/BeBoXGui/termwrap.py</code>

##### P4wnP1 / Kali Linux:
<code>@reboot cd /root/p4wnsolo-joyterm/ && /usr/bin/python3 /root/p4wnsolo-joyterm/go.py</code>

##### Raspberry Pi OS:
<code>@reboot cd /home/pi/p4wnsolo-joyterm/ && /usr/bin/python3 /home/pi/p4wnsolo-joyterm/go.py</code>

The crontab entry above does the following:
* Changes folders into the main working folder using crontab
* Then runs the P4wnP1 OLED Terminal wrapper

## 🎁 Aliases to Add
#### Side project idea – PiPod Shuffle:
Use a quick alias to play MP3 files randomly to mimic and iPod shuffle.

##### Command:

mplayer -loop 0 -shuffle $(cat your_playlist.m3u)

alias music='mplayer --shuffle *

Mplayer

#### or Mimic an iPod shuffle using this command:
https://www.cyberciti.biz/tips/bash-aliases-mac-centos-linux-unix.html
Find a File
I can never remember the syntax for this command.  So why not make an alias for it.

##### Command:

find /home -name *.jpg

#### Modify ping Behavior
I don’t know why I’d do this, but I might:

###### Command:

Stop after sending count ECHO_REQUEST packets:
<code>alias ping=’ping -c 5′</code>
Do not wait interval 1 second, go fast #
<code>alias fastping=’ping -c 100 -s.2′</code>


## ⚰️ Wrap-Up:
To make this script, I basically just modified the terminal.py file from <a href="https://github.com/rm-hull/luma.examples">Luma.examples</a>
1.  Take terminal.py from luma.examples
2.  Find the loop that displays “Line 1, Line 2, Line 3”
3.  Replace it with a loop to read lines from a text file

The result from changing this code was significant:

The terminal.py script now shows output from any program – as long as that program is outputting to a text file.
Since getting programs to output to text in Linux is pretty easy, we can now display pretty much any program’s output on our OLED screen.
 

## Contact
<a href="https://twitter.com/p4wnsolo">@p4wnsolo</a> on Twitter
<a href="https://github.com/p4wnsolo">@p4wnsolo</a> on GitHub
