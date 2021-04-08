# Masking system driver code.
This is cnc code for a raspberry pi controlled relay system, for driving fixed state 240v garage door rollers on a timed basis. this was built many moons ago for a friend who wanted to automate their Cinema screen masking. See https://www.avforums.com/threads/diy-electric-projector-masking.2086836/?fbclid=IwAR1m945RwJg0bJdvYfplcnb-2gT7ogpnFexECx8goUWyeocGzu9guOiJHXg


# Disclaimer:
This is demonstration code. It can not be guaranteed to work correctly. Do not run this on mains voltage. Do not complain to me when you're dead. I accept no responsibility for any anything arising from using this code in any way.  Use at your own risk. Warning. It's not my fault. 



# Hardware setup:
This is built based on  the following setup:
![Wiring](https://github.com/philthetechie/screenmask/blob/main/diagram.png?raw=true)


This is wired for roller motors that have 2 independant wiring loops. one for each direction. 

### This relies on the motors having top and bottom limit switches built in to avoid overrun!!

The idea with the relay layout here is that the main power relays are set to an Open (off) state until the direction relays have been set correctly, and then the Main power relays are Closed (turned on) for the duration of the roll. This - in theory - avoids multiple power lines having power at the same time. I assume that would be bad. 


# Config
Install mysql. Create a user.

Set your pins in config.py, set your sql connection data in config.py.

uncomment https://github.com/philthetechie/screenmask/blob/main/app.py#L198 the first run to create the database tables. 

Comment it out again. 

Yes, there's a better way. Fuck it. I'm too lazy to recode this now. 

run the module directly from your pi's CLI. preferably from a venv. That's an exercise for the reader.

Yes there's a better way. See above.

# Don't die.
