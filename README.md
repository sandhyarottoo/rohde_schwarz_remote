This repo is for controlling the Rohde&Schwarz RTO2014 oscilloscope through python code. 

# Preconditions
Before getting started, you should:

1. **Use a computer connected to the same LAN as the oscilloscope.** The scope should be plugged into the router via an ethernet cable, and your computer should be on this same wifi network.

2. **Install the R&S Visa** at https://www.rohde-schwarz.com/us/applications/rs-visa_56280-148812.html

3. **Install the RSInstrument library.** Type

```
pip install RsInstrument
```
into your command line.

*Note: both R&S visa and RSInstrument should be in a parent directory to where you clone this repo*

4. **Figure out what your scope's IP address is**. On the left of the scope, hit the **Setup** button, then tap on **Network**. The IP address will be listed there. If it is not, check your ethernet connection 

# Now you are ready to control your scope remotely. 

```scope.py``` contains a subclass definition of the RSInstrument class, designed specifically for the RTO2014. It contains functions to set up the oscilloscope's channels with a voltage range, offset and coupling, turn on a manual trigger or an automatic trigger, get a single waveform from the scope and take and save a screenshot from the scope. 

The code is pretty self explanatory and ```example.py``` walks you through how to use it. 


