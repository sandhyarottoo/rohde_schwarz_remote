#Perform a frequency sweep
#author: Sandhya Rottoo (sandhya.rottoo@mail.mcgill.ca)


from scope import *
import os

#initialize the scope
ip = '192.168.0.160'
rto = Scope(f'TCPIP::{ip}::hislip0')
rto.clear_status()
rto.reset()

#input signal is on channel 1, circuit output is on channel 3
rto.setup_chan(1,0.1,3,0,'DCLimit')
rto.setup_chan(3,0.1,3,0,'DCLimit')

#check the coupling
rto.check_coupling(1)
rto.check_coupling(3)


#set up the auto trigger
rto.auto_trigger()


#frequencies to sweep
nfreqs = 16
freqs = np.linspace(10,80,nfreqs)


#perform the sweep (instructions in docstrings of scope.bode_plot)
vpps,phase = rto.bode_plot(3,freqs,'gain7amp0.2_zoom.csv',1,True)


#Don't forget to close the connection
rto.close()

#plot everything
fig, ax1 = plt.subplots()
ax1.plot(freqs,vpps,label = 'Vpp',color = 'k',linestyle = 'dashed')
ax2 = ax1.twinx()
ax2.plot(freqs,phase,label = 'Phase (rad)',color = 'mediumorchid')
ax1.set_xlabel('Frequency (kHz)')
ax1.set_ylabel('Vpp (V)')
ax2.set_ylabel('Phase')
ax1.legend(loc='upper left')
ax2.legend(loc = 'upper right')
plt.show()




