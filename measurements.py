#testing file for unfinished measurement functions
#author: Sandhya Rottoo (sandhya.rottoo@mail.mcgill.ca)


from scope import *
import os


#initialize the scope
ip = '192.168.0.160'
rto = Scope(f'TCPIP::{ip}::hislip0')

# fft = rto.get_fft()
# print(fft)
vpps,freqs = rto.get_measurement(400)
#turn channel 2 off 

# Close the session
rto.close()

plt.plot(vpps,freqs)
plt.show()


