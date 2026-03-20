

from scope import *
import os
savepath = os.getcwd()
fname = savepath + '\screenshot.png'
os.chdir(savepath)
rto = Scope('TCPIP::192.168.0.160::hislip0')
rto.clear_status()
rto.reset()

rto.setup_chan(2,1,1,0,'AC')
#
rto.setup_chan(1,0.1,3,0,'DCLimit')
#

# rto.manual_trigger(2,0.05)
rto.auto_trigger()
xrange = rto.get_xticks()
print(xrange)
#
ch1 = rto.get_data(1)
ch2 = rto.get_data(2)
# rto.screenshot(fname)
# Close the session
rto.close()

t = np.linspace(-1*xrange/2,xrange/2,len(ch1))
print(t)
plt.plot(t,ch1,label = 'Ch1')
plt.plot(t,ch2,label = 'Ch2')
plt.plot(t,ch2)
plt.xlabel('time (s)')
plt.ylabel('voltage (V)')
plt.legend()
plt.show()

