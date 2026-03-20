#Example file of how to control the scope
#author: Sandhya Rottoo (sandhya.rottoo@mail.mcgill.ca)


from scope import *
import os


#initialize the scope
rto = Scope('TCPIP::192.168.0.160::hislip0')
rto.clear_status()
rto.reset()

#setup channels 1 and 2
rto.setup_chan(2,1,1,0,'AC')

rto.setup_chan(1,0.1,3,0,'DCLimit')


#set up the auto trigger
rto.auto_trigger()

#get the time range
xrange = rto.get_xticks()

#get data from channels 1 and 2
ch1 = rto.get_data(1)
ch2 = rto.get_data(2)


#path to save a screenshot to
savepath = os.getcwd()
fname = savepath + '\screenshot.png'
os.chdir(savepath)

#take a screenshot and save it
rto.screenshot(fname)
# Close the session
rto.close()

#plot the data
t = np.linspace(-1*xrange/2,xrange/2,len(ch1))

plt.plot(t,ch1,label = 'Ch1')
plt.plot(t,ch2,label = 'Ch2')
plt.plot(t,ch2)
plt.xlabel('time (s)')
plt.ylabel('voltage (V)')
plt.legend()
plt.show()

