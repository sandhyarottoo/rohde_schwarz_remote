#Subclass of RsInstrument for the RTO2014
#Lots of code borrowed from https://github.com/Rohde-Schwarz/Examples
#Author: Sandhya Rottoo (sandhya.rottoo@mail.mcgill.ca)


from RsInstrument import *
from matplotlib import pyplot as plt
import numpy as np

class Scope(RsInstrument):

    '''
    Subclass of the RsInstrument class for the RTO2014. 
    '''

    def __init__(self,ip):
        '''
        param ip: the IP address of your scope
        Initializes a connection to the RTO2014
        '''
        try:
            super().__init__(ip,reset=False, options='VxiCapable = ON, VisaTimeout = 10000, SelectVisa = rs')
            self.visa_timeout = 100000  # Timeout for VISA Read Operations
            self.opc_timeout = 15000  # Timeout for opc-synchronised operations
            self.instrument_status_checking = True  # Error check after each command
            print(f'Initialized scope {ip}')
            self.chancount = 0
        except:
            print(f'Failed to initialize scope {ip}')
            print('Please check the IP address, and that the R&S visa is installed, and try again')
    def setup_chan(self,channumber,xrange,yrange,offset,coupling,xpoints = 20002):

        '''

        :param channumber: channel number (1,2,3,4)
        :param xrange: aquisition range in seconds
        :param yrange: voltage scale in V
        :param offset: voltage offset in V
        :param coupling: scope coupling. options: AC, DC (50 ohm) and DCLimit (1MOhm)
        :param xpoints: number of points to sample
        example usage:

        rto.setup_chan(1,0.01,2,0,AC)
        will set up the channel 1 for a 10 ms acquisition, with a 2V range, 0 offset and AC coupling
        '''
        #check that the inputs are all valid
        if channumber not in [1,2,3,4]:
            raise ValueError(f"Invalid channel number: {channumber}. Please select from 1,2,3,4")
        if coupling not in ['AC','DC','DCLimit']:
            raise ValueError(f'Invalid coupling: {coupling}. Please select from AC,DC,DCLimit')
        print(f'Setting up channel {channumber} \n acquisition over: {xrange}s '
              f'\n voltage range: {yrange} V'
              f'\n DC offset: {offset}V \n coupling: {coupling}V')
        if self.chancount == 0:
            self.xrange = xrange
        else:
            if xrange != self.xrange:
                print(f'xrange already initialized with another channel. Setting xrange to {self.xrange}')
       
        #setup the channel
        self.write_str(f"ACQ:POIN:AUTO RECL")  # Define Horizontal scale by number of points
        self.write_str(f"TIM:RANG {self.xrange}")  # 10ms Acquisition time
        self.write_str(f"ACQ:POIN {xpoints}")  # 20002 X points
        self.write_str(f"CHAN{channumber}:RANG {yrange}")  # Horizontal range 2V
        self.write_str(f"CHAN{channumber}:POS {offset}")  # Offset 0
        self.write_str(f"CHAN{channumber}:COUP {coupling}")  # Coupling AC 1MOhm
        self.write_str(f"CHAN{channumber}:STAT ON")  # Switch Channel 1 ON
        self.chancount += 1

    def turn_channel_off(self,channumber):
        # turns the channel off
        self.write_str(f'CHAN{channumber}:STAT OFF')

    def manual_trigger(self,channumber,level,mode = 'NORMal',type = "EDGE;:TRIG1:EDGE:SLOP POS"):
        '''
        Set up a manual trigger for a given channel and trigger level
        :param channumber: channel number (1,2,3,4)
        :param level: trigger level in V
        :param mode: trigger mode (AUTO or NORMal)
        :param type: trigger type (EDGE or SLOP)

        '''
        self.write_str(f"TRIG1:SOUR CHAN{channumber}")  # Trigger source CH1
        self.write_str(f"TRIG1:TYPE {type}")  # Trigger type Edge Positive
        self.write_str(f"TRIG1:LEV1 {level}")  # Trigger level 40mV
        self.write_str(f'TRIGger1:MODe {mode}')
        self.write_str('SINGle')
        self.write_str('AUToscale')  # Perform auto scaling
        self.query_opc()  # Using *OPC? query waits until all the instrument settings are finished

    def auto_trigger(self):
        '''
        Set the scope to trigger automatically (equivalent of the autoset button on the top left)
        '''
        self.write_str(f"TRIG1:MODE AUTO")  # Trigger Auto mode in case of no signal is applied


    def get_data(self,channumber,n = 1,save = False,plot = False,savepath = None):
        '''
        Gets the measurement data from the scope for a given channel and returns it
        Option to aquire many waveforms and then average them
        :param channumber: channel number (1,2,3,4)
        :return:
        '''
        self.write_str(f'ACQuire:COUNt {n}')  # Acquire 20 waveforms to calculate average waveform
        self.write_str(f"TRIGger1:SOURce CHAN{channumber}")  # Define trigger source
        self.write_str('TRIGger1:MODe NORMal')  # Trigger mode is normal
        self.write_str('SINGle')  # Single trigger operations
        self.write_str('AUToscale')  # Perform auto scaling
        self.query_opc()  # Check for command completion
        trace = self.query_bin_or_ascii_float_list(f'FORM ASC;:CHAN{channumber}:DATA?')  # Query ascii array of floats
        return trace

    def get_xticks(self):
        '''
        For plotting. Gets the time of a waveform
        '''
        xrange = float(self.query_str('TIM:RANG?'))
        self.query_opc()
        return xrange

    def check_coupling(self,channumber):
        #check the coupling of a channel
        #you can do this for any of the parameters in the same format
        #remember to always put self.query_opc() at the end
        coup = self.query_str(f'CHAN{channumber}:COUP?')
        self.query_opc()
        print(f'Coupling for channel {channumber}: {coup} ')

    def screenshot(self,path_to_save):
        '''
        Takes a screenshot of the scope and saves it to your computer
        '''
        file_path_instr = r'c:\Temp\Device_Screenshot.png'

        self.write_str("HCOPy:DEVice1:LANGuage PNG")
        self.write_str(f"MMEMory:NAME '{file_path_instr}'")
        self.write_str_with_opc("HCOPy:IMMediate1")
        self.read_file_from_instrument_to_pc(file_path_instr, path_to_save)

        self.query_opc()

        print(f"\nSaved screenshot to {path_to_save}")