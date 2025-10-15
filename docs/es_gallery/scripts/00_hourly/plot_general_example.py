# -*- coding: utf-8 -*-
"""
Thumbnail name
===================================

This text shows when hovering over the thumbnail.
"""

import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 2 * np.pi, 100)
y = np.sin(x)

plt.plot(x, y)
plt.xlabel(r'$x$')
plt.ylabel(r'$\sin(x)$')
# To avoid matplotlib text output
plt.show()


print('This example shows a sin plot!')
