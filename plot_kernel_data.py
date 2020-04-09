import os
import matplotlib.pyplot as plt
import statistics
import scipy.signal as dsp
import numpy as np

def get_array(x):
    x = x.replace('[', '')
    x = x.replace(']', '')
    x = x.split(',')
    x = [float(el) for el in x]
    return x

time = [];
load_est = []
load = []
uc = []
freq = [];
freq_next = [];
P = [];
theta = [];
stop = 1;
with open('data.txt') as f:
    lines = f.readlines()
    for line in lines:
        line_split = line.split(';')
        #if stop:
        #    print(line_split)
        #    stop = 0
        time.append(float(line_split[0])+float(line_split[1])/1000000)
        load.append(float(line_split[3]))
        load_est.append(float(line_split[4]))
        uc.append(float(line_split[5]))
        freq.append(float(line_split[6]))
        freq_next.append(float(line_split[7]))
        theta.append(get_array(line_split[8]))
        P.append(get_array(line_split[13]))

print(statistics.mean(load));
print(statistics.mean(load_est));

a = np.array([1])
l = 1;
b = np.ones(l, dtype=float)/l
a.astype(float)
load_est = dsp.lfilter(b, a, load_est);
load= dsp.lfilter(b, a, load);

#N=500
#plt.figure(0)
#axes = plt.gca()
#axes.set_ylim([0,200])
#plt.plot(time, load, label='load');
#plt.plot(time, load_est, label='load_est');
#plt.plot(time, uc, label='uc');
#plt.grid()
#plt.legend(loc='upper left')

plt.figure(1)
plt.subplot(4, 1, 1)
axes = plt.gca()
axes.set_ylim([0,200])
plt.plot(time, load, label='load');
plt.plot(time, load_est, label='load_est');
plt.plot(time, uc, label='uc');
plt.grid()
plt.legend(loc='upper left')

plt.subplot(4, 1, 2)
axes = plt.gca()
axes.set_ylim([0,5000000])
plt.plot(time, freq, label='u');
plt.plot(time, freq_next, label='v');
plt.grid()
plt.legend(loc='upper left')

plt.subplot(4, 1, 3)
plt.plot(time, theta);
plt.grid()
plt.legend(["theta[0](a1)", "theta[1](b0)"], loc='upper left')

plt.subplot(4, 1, 4)
plt.plot(time, P);
plt.legend(["P[0]", "P[1]","P[2]","P[3]"], loc='upper left')
plt.grid()
plt.show()


