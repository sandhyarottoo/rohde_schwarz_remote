#Example file of how to control the scope
#author: Sandhya Rottoo (sandhya.rottoo@mail.mcgill.ca)


from scope import *
import os


#initialize the scope
ip = '192.168.0.160'
rto = Scope(f'TCPIP::{ip}::hislip0')
rto.clear_status()
rto.reset()

#setup channels 1
rto.setup_chan(1,1,1,0,'AC')

#set up the auto trigger
rto.auto_trigger()

#get the time range
xrange = rto.get_xticks()

#get data from channels 1 and 2
ch1 = rto.get_data(1)
# ch2 = rto.get_data(2)

rms = rto.get_measurement(1)
print(rms)
#turn channel 2 off 

# Close the session
rto.close()


