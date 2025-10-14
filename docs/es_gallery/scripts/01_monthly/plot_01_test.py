# -*- coding: utf-8 -*-
"""
Monthly example
===================================

This could be an example for the monthly version of EnergyScope.
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
