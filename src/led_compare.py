#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 20:48:58 2024

@author: janmejoyarch
"""

from astropy.io import fits
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import numpy as np
import glob
import os

led='255'
save=True
proj_path= os.path.expanduser('~/Dropbox/Janmejoy_SUIT_Dropbox/writing_and_presentations/SUIT_meetings/payload_baking/baking_closeout_project')
datelist=['2023/11/23', '2023/12/05', '2023/12/06', '2024/02/24', '2024/03/20', '2024/05/17', '2024/06/25', '2024/07/02']
ls_typ1, ls_typ2= [], [] #aa/aa00, 55/5500

if led=='355':
    typ1_id, typ2_id= 'aa00', '5500'
elif led=='255':
    typ1_id, typ2_id= '55', 'aa'


for date in datelist:
    path= os.path.join('/home/janmejoyarch/sftp_drive/suit_data/level0fits/', date, 'led*/*')
    filelist=sorted(glob.glob(path))
    for file in filelist:
        hdu= fits.open(file)[0]
        if hdu.header['LEDONOFF'].endswith(typ1_id) and hdu.header['QDESC']=='Complete Image': #355
            print(typ1_id, os.path.basename(file))
            ls_typ1.append(file)

        elif hdu.header['LEDONOFF'].endswith(typ2_id) and hdu.header['QDESC']=='Complete Image': #355
            print(typ2_id, os.path.basename(file))
            ls_typ2.append(file)
            break
        
n=0
for typ1, typ2 in zip(ls_typ1, ls_typ2):
    n=n+1
    plt.figure()
    plt.subplot(1,2,1)
    plt.imshow(fits.open(typ1)[0].data, origin='lower', norm=LogNorm())
    plt.title('Lev0_'+ os.path.basename(typ1).split('_')[5])
    plt.subplot(1,2,2)
    plt.imshow(fits.open(typ2)[0].data, origin='lower', norm=LogNorm())
    plt.title('Lev0_'+ os.path.basename(typ2).split('_')[5])
    if save: plt.savefig(os.path.join(proj_path,'tmp/Lev0_'+str(n)+'_'+led+'nm.png'), dpi=300)

        