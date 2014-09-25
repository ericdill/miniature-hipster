#!/usr/bin/env python
# -*- coding: utf-8 -*-

################################################################################
# imports
from __future__ import unicode_literals
import os
from collections import deque
# matplotlib
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.collections import PolyCollection
# scipy/numpy
import numpy as np
from scipy.signal import savgol_filter
from scipy.interpolate import UnivariateSpline
# pandas
import pandas as pd
from pandas import DataFrame, Series
from pprint import pprint
################################################################################

__author__ = 'edill'

#### DATA FOLDER DIRECTORY #####################################################
folder = 'C:\\DATA\\New folder\\Data_4_Eric\\SCAN_Xr0'
folder = 'C:\\DATA\\New folder\\Data_4_Eric\\SCAL_alongX'

#### PLOTTING OPTIONS ##########################################################
x_label = '2-theta (degrees)'
y_label = 'Frame number'
z_label = 'Intensity (arb.)'
min_x = 42
max_x = 60
min_y = None
max_y = None
min_z = 0
max_z = None
alpha = 1
smooth = True
smooth_window_length = 91
smooth_poly_order = 7  # must be odd!
space_between_frames = 1  # y-spacing for each line
# color = cm.datad['winter']
# print(color)
color = 'hot_r'
cstart = 0.3
cstop = 0.7

print_color_options = True
if print_color_options:
    print(list(cm.datad))

#### RUNTIME BEHAVIOR ##########################################################
# init some parameters
norm = cm.colors.Normalize(vmin=0, vmax=1)
files = os.listdir(folder)
pprint(files)
data = DataFrame()
smoothed = DataFrame()

# init the defaults
if min_y is None:
    min_y = 0
if max_y is None:
    max_y = len(files)

for fname in files[min_y:max_y]:
    with open(folder + os.sep + fname, 'r') as f:
        # data.append(np.asarray([line.split() for line in f.next()]).T)
        x, y = np.asarray([[float(val) for val in line.split()] for line in f]).T
        val = Series(y, index=x)
        data[fname] = Series(y, index=x)

# init the defaults
if min_x is None:
    min_x = float(data.index[0])
if max_x is None:
    max_x = float(data.index[-1])

# apply x-axis filtering
data = data[data.index > min_x]
data = data[data.index < max_x]
indices = data.index

if smooth:
    # smooth the data into a new data frame
    for d in data:
        # smooth data
        vals = data[d].values
        y = savgol_filter(vals, smooth_window_length, smooth_poly_order, mode='nearest').tolist()
        len(y)
        smoothed[d] = Series(y, indices)

    smoothed.ix[0] = 0
    smoothed.ix[-1] = 0
    to_plot = smoothed

else:
    data.ix[0] = 0
    data.ix[-1] = 0
    to_plot = data

# set the min and max values for z after smoothing
if min_z is None:
    min_z = np.min([np.min(data[col_name]) for col_name in data])
else:
    for col_name in to_plot:
        colvals = to_plot[col_name].values
        colvals[colvals < min_z] = min_z
if max_z is None:
    max_z = np.max([np.max(data[col_name]) for col_name in data])
else:
    for col_name in to_plot:
        colvals = to_plot[col_name].values
        colvals[colvals > max_z] = max_z


poly_pairs = deque()
# create the color map
rgba = cm.ScalarMappable(cmap=color, norm=norm)
colors = rgba.to_rgba(x=np.linspace(cstart, cstop,
                                    len(to_plot.columns)),
                      alpha=alpha)

for idx, d in enumerate(to_plot):
    vals = to_plot[d]
    poly_pairs.append([(x, y) for x, y in zip(indices, to_plot[d].values)])

# create the collection of polygons to plot
poly = PolyCollection(list(poly_pairs), facecolors=colors)

# init the matplotlib figures
fig = plt.figure()
ax3 = Axes3D(fig)

# set the offset of each polygon
nz = len(data) * space_between_frames
zs = np.arange(0, nz, space_between_frames)
# add the polygons to the
ax3.add_collection3d(poly, zs=zs, zdir='y')
ax3.set_xlabel(x_label)
ax3.set_ylabel(y_label)
ax3.set_zlabel(z_label)
ax3.set_xlim3d(min_x, max_x)
ax3.set_ylim3d(min_y, max_y)
ax3.set_zlim3d(min_z, max_z)

# show the plot
plt.show()