#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  7 20:46:41 2020

@author: inderpreet
"""
import matplotlib.pyplot as plt
import numpy as np
import netCDF4

from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)
from typhon.retrieval.qrnn import set_backend, QRNN
set_backend("pytorch")
import stats as S
from ici import iciData
plt.rcParams.update({'font.size': 26})
#%% calibration plot
def calibration(y_pre, y0, im, quantiles):

    intervals = []
    for i in range(1, 6):
        intervals.append(quantiles[i] - quantiles[0] )
    a0 = 0
    a1 = 0
    a2 = 0
    a3 = 0
    a4 = 0
    a5 = 0
    a6 = 0
    for i in im:

        if np.logical_and(y0[i] > y_pre[i, 0] ,  y0[i] <=y_pre[i, 1]):
                   a1 += 1
        if np.logical_and(y0[i] > y_pre[i, 0] ,  y0[i] <= y_pre[i, 2]):
                   a2 += 1               
        if np.logical_and(y0[i] > y_pre[i, 0] ,  y0[i] <= y_pre[i, 3]):
                   a3 += 1
        if np.logical_and(y0[i] > y_pre[i, 0] ,  y0[i] < y_pre[i, 4]):
                   a4 += 1
        if np.logical_and(y0[i] > y_pre[i, 0] ,  y0[i] < y_pre[i, 5]):
                   a5 += 1
        if np.logical_and(y0[i] > y_pre[i, 0] ,  y0[i] < y_pre[i, 6]):
                   a6 += 1
    return a1, a2, a3, a4, a5,a6, intervals 
#%% input parameters
depth     = 4
width     = 128
quantiles = np.array([0.002, 0.03, 0.16, 0.5, 0.84, 0.97, 0.998])
batchSize = 128

target = 'I1V'


inChannels = np.array(['I1V', 'I2V', 'I3V', 'I5V' , 'I6V', 'I7V', 'I8V', 'I9V', 'I10V', 'I11V'])
#inChannels = np.array(['I1V', 'I2V', 'I3V', 'MWI-15', 'MWI-16', 'I5V', 'I6V', 'I7V', 'I8V', 'I9V', 'I10V', 'I11V', 'I11H'])
inChannels = np.array([target, 'I5V' , 'I6V', 'I7V', 'I8V', 'I9V', 'I10V', 'I11V'])
i183, = np.argwhere(inChannels == target)[0]

binstep = 0.5
bins = np.arange(-20, 15, binstep)
iq = np.argwhere(quantiles == 0.5)[0,0]

#%% read input data
data = iciData("TB_ICI_test.nc", 
               inChannels, target, 
               batch_size = batchSize)  

file = 'qrnn_ici_%s_%s_%s_single.nc'%(depth, width, target)
print (file)
qrnn = QRNN.load(file)

y_pre, y_prior, y0, y, y_pos_mean = S.predict(data, qrnn, add_noise = True)
#%% plot calibration curves
# calibration plot data with correction greater than 15K

fig, ax = plt.subplots(1, 1, figsize = [8,8])   

im = np.arange(0, y0.size, 1)
a1, a2, a3, a4, a5, a6, intervals  = calibration(y_pre, y0, im, quantiles)
    

(ax.plot(intervals[:], [ a1/len(y0[:]), a2/len(y0[:]), a3/len(y0[:]), 
                           a4/len(y0[:]), a5/len(y0[:]),
                          ], 'r.-', ms = 15, linewidth = 2.5))

im = np.where(np.abs(y_pre[:, iq] - y_prior[:, i183]) > 5 )[0]
a1, a2, a3, a4, a5, a6, intervals  = calibration(y_pre, y0, im, quantiles)     

(ax.plot(intervals[:], [ a1/len(y0[im]), a2/len(y0[im]), a3/len(y0[im]), 
                           a4/len(y0[im]), a5/len(y0[im]),
                          ], 'b.-', ms = 15, linewidth = 2.5))


# im = np.where(np.abs(y_pre[:, iq] - y_prior[:, i183]) > 15 )[0]
# a1, a2, a3, a4, a5, a6, intervals  = calibration(y_pre, y0, im, quantiles)     

# (ax.plot(intervals[:], [ a1/len(y0[im]), a2/len(y0[im]), a3/len(y0[im]), 
#                            a4/len(y0[im]), a5/len(y0[im]),
#                           ], 'g.-', ms = 15, linewidth = 2.5))

#%% read input data
inChannels = np.array(['I1V', 'I2V', 'I3V', 'I5V' , 'I6V', 'I7V', 'I8V', 'I9V', 'I10V', 'I11V'])
data = iciData("TB_ICI_test.nc", 
                inChannels, target, 
                batch_size = batchSize)  

x_noise = data.add_noise(data.x, data.index)


file = 'qrnn_ici_%s_%s_%s.nc'%(depth, width, target)
print (file)
qrnn = QRNN.load(file)

y_pre, y_prior, y0, y, y_pos_mean = S.predict(data, qrnn, add_noise = True)

im = np.arange(0, y0.size, 1)
a1, a2, a3, a4, a5, a6, intervals  = calibration(y_pre, y0, im, quantiles)
    

(ax.plot(intervals[:], [ a1/len(y0[im]), a2/len(y0[im]), a3/len(y0[im]), 
                            a4/len(y0[im]), a5/len(y0[im]),
                          ], 'g.-', ms = 15, linewidth = 2.5))

im = np.where(np.abs(y_pre[:, iq] - y_prior[:, i183]) > 5 )[0]
a1, a2, a3, a4, a5, a6, intervals  = calibration(y_pre, y0, im, quantiles)     

(ax.plot(intervals[:], [ a1/len(y0[im]), a2/len(y0[im]), a3/len(y0[im]), 
                            a4/len(y0[im]), a5/len(y0[im]),
                          ], 'y.-', ms = 15, linewidth = 2.5))


# im = np.where(np.abs(y_pre[:, iq] - y_prior[:, i183]) > 15 )[0]
# a1, a2, a3, a4, a5, a6, intervals  = calibration(y_pre, y0, im, quantiles)     

# (ax.plot(intervals[:], [ a1/len(y0[im]), a2/len(y0[im]), a3/len(y0[im]), 
#                             a4/len(y0[im]), a5/len(y0[im]),
#                           ], 'm.-', ms = 15, linewidth = 2.5))


x = np.arange(0,1.2,0.2)
y = x
ax.plot(x, y, 'k:', linewidth = 1.5)
ax.set(xlim = [0, 1], ylim = [0,1])
ax.set_aspect(1.0)
ax.set_xlabel("Predicted frequency")
ax.set_ylabel("Observed frequency")
ax.xaxis.set_minor_locator(MultipleLocator(0.2))
ax.grid(which = 'both', alpha = 0.2)
fig.savefig('Figures/calibration_plot_%s'%target)

(ax.legend(["QRNN-simple", "QRNN-simple(5K)", "QRNN-all", "QRNN-all(5K)"],
            prop={'size': 22}, frameon = False))  

fig.savefig("Figures/calibration_QRNN_%s.pdf"%target)