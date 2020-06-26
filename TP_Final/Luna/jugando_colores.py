# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 12:14:28 2020

@author: Luna
"""

import matplotlib.pyplot as plt
import numpy as np

x = np.arange(0,500,1)
y = np.sin(x)
c = x
plt.scatter(x,y,cmap = 'viridis',c=c)
cbar = plt.colorbar()
cbar.set_label('Color Intensity')