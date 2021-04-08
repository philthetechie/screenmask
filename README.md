# Masking system driver code.
This is cnc code for a raspberry pi controlled relay system, for driving fixed state 240v garage door rollers on a timed basis.

# Disclaimer:
This is demonstration code. It can not be guaranteed to work correctly. Do not run this on mains voltage. Do not complain to me when you're dead. I accept no responsibility for any anything arising from using this code in any way.  Use at your own risk. Warning. It's not my fault. 



# Hardware setup:
This is built based on  the following setup:
![Wiring](https://github.com/philthetechie/screenmask/blob/main/diagram.png?raw=true)


This is wired for roller motors that have 2 independant wiring loops. one for each direction. 

The idea with the relay layout here is that the main power relays are set to an Open (off) state until the direction relays have been set correctly, and then the Main power relays are Closed (turned on) for the duration of the roll. This - in theory - avoids multiple power lines having power at the same time. I assume that would be bad. 


# Config
Set your pins in config.py, run the module directly from your pi's CLI. preferably from a venv. That's an exercise for the reader. 

# Don't die.