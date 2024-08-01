#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 26 11:16:10 2024
-To plot and analyze the ratio and noise images.
@author: janmejoyarch
"""

from astropy.io import fits
import matplotlib.pyplot as plt
import os
import numpy as np

proj_path= os.path.expanduser('~/Dropbox/Janmejoy_SUIT_Dropbox/writing_and_presentations/SUIT_meetings/payload_baking/baking_closeout_project')
ref= fits.open(os.path.join(proj_path, 'data/raw/SUT_UNP_9999_999999_Lev1.0_2023-11-23T08.04.31.798_B011BB02.fits'))[0].data
data= fits.open(os.path.join(proj_path, 'data/raw/SUT_T24_0701_000371_Lev1.0_2024-04-22T22.30.48.532_B011BB02.fits'))[0].data
plt.imshow(ref, origin='lower'); plt.colorbar()
num_1= data[0:1500,2040:2055]
np.savetxt(os.path.join(proj_path,'reports/numerator_[0:1500,2040:2055].csv'), num_1, delimiter=',')
denom_1= ref[0:1500:,2040:2055]
np.savetxt(os.path.join(proj_path,'reports/denominator_[0:1500,2040:2055].csv'), denom_1, delimiter=',')


plt.figure()
plt.plot(data[500, 2040:2055], '-o', label= 'numerator [row 500]\n Lev1.0_2023-11-23 255 nm')
plt.plot(ref[500, 2040:2055], '-o', label= 'denominator [row 500]\n Lev1.0_2024-04-22 255 nm')
plt.xticks(ticks= np.arange(15), labels=np.arange(2040, 2055))
plt.xlabel('Column Number')
plt.ylabel('Counts [row 500]')
plt.legend()
plt.title('Line profile')
plt.grid(alpha=0.3)


'''
 In the original images from which the ratio image in the third slide of the ppt was derived, what were the counts in?

Numerator image columns 2040 to 2047
Numerator image columns 2048 to 2055
Denominator image columns 2040 to 2047
Denominator image columns 2048 to 2055
'''