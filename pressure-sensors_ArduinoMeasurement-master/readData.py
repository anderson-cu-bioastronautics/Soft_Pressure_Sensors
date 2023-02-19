import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import rcParams
import math
from scipy.stats import linregress
from sklearn.metrics import mean_squared_error



def find_nearest(array,value):
    idx = np.searchsorted(array, value, side="left")
    if idx > 0 and (idx == len(array) or math.fabs(value - array[idx-1]) < math.fabs(value - array[idx])):
        return idx-1
    else:
        return idx

plt.style.use('seaborn-poster')
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Roboto']
params = {'axes.labelsize': 32,'axes.titlesize':20, 'font.size': 20, 'legend.fontsize': 40, 'xtick.labelsize': 34, 'ytick.labelsize':34}
rcParams.update(params)



directory = 'Data/sensor10/'
lines = [line.rstrip('\n') for line in open(directory+'Report.xls')]
fData = []
fTime = []


for line in lines:
    try:
        [t_fTime,t_fValue] = line.split('\t')
        t_fTime = np.float(t_fTime)
        t_fValue = np.float(t_fValue)
        t_fValue = -10 * t_fValue / (np.pi * .7 * .7)
        fData.append(t_fValue)
        fTime.append(t_fTime)
    except:
        pass

sData = [line.rstrip('\n') for line in open(directory+'data.txt')]
sTime = [line.rstrip('\n') for line in open(directory+'time.txt')]
sData = [np.float(data) for data in sData]
sTime = [np.float(data) for data in sTime]

s_ind = np.nonzero(sData)[0][0]
sTime[:] = [x - sTime[s_ind] for x in sTime]

f_ind = np.nonzero(fData)[0][0]
fTime[:] = [x - fTime[f_ind] for x in fTime]
#f_ind = np.nonzero(fData)[0][0]
#fData = fData[f_ind:-1]
#fTime = fTime[f_ind:-1]

sBroad= np.empty([1,0])

for fidx, time in enumerate(fTime):
    sidx = find_nearest(sTime,time)
    sBroad = np.append(sBroad,sData[sidx])
    
slope, intercept, r_value, p_value, std_err = linregress(fData,sBroad)
xNew = np.linspace(0,np.amax(fData),len(fData))
yNew = xNew * slope + intercept
rms = math.sqrt(mean_squared_error(sBroad, yNew))
print('R^2 Value: ',r_value**2)
print('RMS Value: ', rms)

#split into sections to find sectional residuals
#sections = np.array([[0,9],[9,19],[19,30],[30,55]]) #15-7
sections = np.array([[0,15],[15,32],[32,51]]) #15-9
#sections = np.array([[0,7],[7,16],[16,22],[22,50]]) #12-1
#sections = np.array([[0,17],[17,41],[41,75]]) #12-4

sections_idx = np.empty_like(sections)
fData_seg = np.empty((len(sections_idx)))
for idx,section in enumerate(sections):
    f1 = find_nearest(fTime,section[0])
    f2 = find_nearest(fTime,section[1])
    sections_idx[idx] = [f1,f2]
    
    
for idx, section in enumerate(sections_idx):
    f1 = section[0]
    f2 = section[1]
    fData_seg = fData[f1:f2]
    sBroad_seg = sBroad[f1:f2]
    slope, intercept, r_value, p_value, std_err = linregress(fData_seg,sBroad_seg)
    xNew = np.linspace(0,np.amax(fData_seg),len(fData_seg))
    yNew = xNew * slope + intercept
    rms = math.sqrt(mean_squared_error(sBroad_seg, yNew))
    print('Section', idx, ':')
    print('R^2 Value: ',r_value**2)
    print('RMS Value: ', rms)
    
w, h = matplotlib.figure.figaspect(0.9)
fig = plt.figure(1,figsize=(w,h))
plt.gcf().subplots_adjust(left=0.14)
plt.gcf().subplots_adjust(bottom=0.12)
ax = fig.add_subplot(111)
fLine = ax.plot(fTime,fData,'b-', label = 'Applied Pressure')
#ax.set_ylabel('Pressure (kPa)')

ax2 = ax.twinx()
sLine = ax2.plot(sTime,sData,'r-', label = 'Sensor Output')
#ax2.set_ylabel('Resistance (ohms)')

lns = fLine + sLine
labs = [l.get_label() for l in lns]
ax.legend(lns,labs, loc=0)

ax.set_ylim((0,300))
ax2.set_ylim((0,6.5))
ax.set_xlim((0,70))
ax.grid(True)
#ax.set_xlabel('Time (s)')
#plt.title(directory)

for idx, section in enumerate(sections_idx):
    xtime = fTime[section[0]:section[1]]
    ydata = np.full((len(xtime)),300)
    ax.plot(xtime,ydata)
    ax.fill_between(xtime,ydata,alpha=0.2)


#plt.show()
fig.savefig(directory+'figure.pdf', transparent=True)
#fig.savefig(directory+'figure.png')
np.savetxt(directory+'sensor.csv',np.vstack(([sData],[sTime])),delimiter=",")
np.savetxt(directory+'force.csv',np.vstack(([fData],[fTime])),delimiter=",")

w, h = matplotlib.figure.figaspect(0.8)
fig = plt.figure(1,figsize=(w,h))

fig2 = plt.figure(2, figsize=(w,h))
ax3 = fig2.add_subplot(111)
fLine = ax3.plot(fData,sBroad,'o', xNew, yNew)
#ax3.set_xlabel('Pressure (kPa)')
#ax3.set_ylabel('Resistance (ohms)')
ax3.set_xlim((0,20))
ax3.set_ylim((0,8))
fig2.savefig(directory+'figure2.pdf', transparent=True)
#fig2.savefig(directory+'figure2.png')
#plt.show()