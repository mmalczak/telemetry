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

x_beg = 00;
x_end = 100;

time = [];
load_est = []
load = []
uc = []
freq = [];
freq_next = [];
R = [];
S = [];
T = [];
D = [];
P = [];
phi_P_phi = [];
theta = [];
stop = 1;
with open('data.txt') as f:
    lines = f.readlines()
    for line in lines:
        line_split = line.split(';')
        #if stop:
        #    print(line_split)
        #    stop = 0
        time.append(float(line_split[0])+float(line_split[1])/1000000000)
        load.append(float(line_split[3]))
        load_est.append(float(line_split[4]))
        uc.append(float(line_split[5]))
        freq.append(float(line_split[6]))
        freq_next.append(float(line_split[7]))
        theta.append(get_array(line_split[8]))
        R.append(get_array(line_split[9]))
        S.append(get_array(line_split[10]))
        T.append(get_array(line_split[11]))
        D.append(get_array(line_split[12]))
        P.append(get_array(line_split[13]))
        phi_P_phi.append(get_array(line_split[14]))

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


N = len(time);
x_beg = int(N*x_beg/100);
x_end = int(N*x_end/100);

N_subplot = 6;

plt.figure(1)
sp = plt.subplot(N_subplot, 1, 1)
sp.set_title("Output")
axes = plt.gca()
axes.set_ylim([0,200])
plt.plot(time[x_beg:x_end], load[x_beg:x_end], label='y');
#plt.plot(time[x_beg:x_end], load_est[x_beg:x_end], label='y_est');
plt.plot(time[x_beg:x_end], uc[x_beg:x_end], label='uc');
plt.grid()
plt.legend(loc='upper left')

#sp = plt.subplot(N_subplot, 1, 2)
#sp.set_title("Input")
#axes = plt.gca()
##axes.set_ylim([0,5000000])
#plt.plot(time[x_beg:x_end], freq_next[x_beg:x_end], label='v');
#plt.plot(time[x_beg:x_end], freq[x_beg:x_end], label='u');
#plt.grid()
#plt.legend(loc='upper left')

sp = plt.subplot(N_subplot, 1, 2)
sp.set_title("Input scaled")
axes = plt.gca()
axes.set_ylim([0,5000000])
plt.plot(time[x_beg:x_end], freq_next[x_beg:x_end], label='v');
plt.plot(time[x_beg:x_end], freq[x_beg:x_end], label='u');
plt.grid()
plt.legend(loc='upper left')


sp = plt.subplot(N_subplot, 1, 3)
sp.set_title("Estimated parameters")
plt.plot(time[x_beg:x_end], theta[x_beg:x_end]);
plt.grid()
leg = []
for i in range(len(theta[0])):
    leg.append("theta["+str(i)+"]")
plt.legend(leg, loc='upper left')

#sp = plt.subplot(N_subplot, 1, 5)
#sp.set_title("Covariance matrix")
#plt.plot(time[x_beg:x_end], P[x_beg:x_end]);
##leg = []
##for i in range(len(theta)):
##    leg.append("P["+str(i)+"]")
##plt.legend(leg, loc='upper left')

sp = plt.subplot(N_subplot, 1, 4)
sp.set_title("Controller")
axes = plt.gca()
axes.set_ylim([-10,10])
plt.plot(time[x_beg:x_end], R[x_beg:x_end]);
plt.plot(time[x_beg:x_end], S[x_beg:x_end]);
plt.plot(time[x_beg:x_end], T[x_beg:x_end]);
leg = []
for i in range(len(R[0])):
    leg.append("R["+str(i)+"]")
for i in range(len(S[0])):
    leg.append("S["+str(i)+"]")
for i in range(len(T[0])):
    leg.append("T["+str(i)+"]")
plt.legend(leg, loc='upper left')

sp = plt.subplot(N_subplot, 1, 5)
sp.set_title("Controller")
axes = plt.gca()
axes.set_ylim([-10,10])
plt.plot(time[x_beg:x_end], D[x_beg:x_end]);
leg = []
for i in range(len(D[0])):
    leg.append("D["+str(i)+"]")
plt.legend(leg, loc='upper left')

sp = plt.subplot(N_subplot, 1, 6)
sp.set_title("phi_P_phi")
axes = plt.gca()
#axes.set_ylim([-20000,-50000])
plt.plot(time[x_beg:x_end], phi_P_phi[x_beg:x_end]);
plt.hlines(1000, time[x_beg], time[x_end-1]);
#leg = []
#for i in range(len(D[0])):
#    leg.append("D["+str(i)+"]")
#plt.legend(leg, loc='upper left')

plt.grid()
plt.show()

#plt.figure(2)
#sp = plt.subplot()
#ax = plt.gca()
#ax.set_xlim((-5, 5))
#ax.set_ylim((-2.5, 2.5))
#sp.set_title("Model poles and zeros")
#zeros_re = []
#zeros_im = []
#poles_re = []
#poles_im = []
##theta = theta[0:1]
#for idx, theta_el in enumerate(theta):
#    A = [1] + theta_el[0:2]
#    B = theta_el[2:]
#    z = np.roots(B)
#    p = np.roots(A)
#    zeros_re.append(z.real)
#    zeros_im.append(z.imag)
#    poles_re.append(p.real)
#    poles_im.append(p.imag)
#circle1 = plt.Circle((0, 0), 1, fill=False)
#ax.add_artist(circle1)
#plt.scatter(poles_re, poles_im, marker = 'x', color='r')
#plt.scatter(zeros_re, zeros_im, marker = 'o', color='none', edgecolor='b')
#plt.grid()
#plt.show()
