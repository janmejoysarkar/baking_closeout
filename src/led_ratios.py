#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 21 19:19:46 2024

@author: janmejoyarch
"""
import os
from astropy.io import fits
import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np
import datetime

def prep_header(fname, ref_img, led_wl, data_img, comment):
    header=fits.Header()
    header['FNAME']=(fname, 'LED ID for SUIT')
    header['MFG_DATE']= (str(datetime.date.today()), "Date of generating this image")
    header['REF_IMG']= (ref_img, 'Reference Image')
    header['DATA_IMG']= (data_img, 'Reference Image')
    header['LED']= (led_wl, 'LED wavelength in nm' )
    header['COMMENTS']=(comment)
    return (header)

def stats(data):
    s=10
    crop_list=[ data[1024-s:1024+s, 1024-s:1024+s],
                data[3072-s:3072+s, 1024-s:1024+s],
                data[3072-s:3072+s, 3072-s:3072+s],
                data[1024-s:1024+s, 3072-s:3072+s]
                ]
    print("Pos Mean(e-) Noise(e-) NSR(%)")
    for i in range(len(crop_list)):
        crop=crop_list[i]
        mean= np.mean(crop*3)
        noise= np.sqrt(mean)
        snr= noise/mean
        print(i+1, round(mean, 0), round(noise, 1), round(snr*100, 1))

if __name__=='__main__':
    
    proj_path= os.path.expanduser('~/Dropbox/Janmejoy_SUIT_Dropbox/writing_and_presentations/SUIT_meetings/payload_baking/baking_closeout_project')
    plot=True
    save=True
    sav= os.path.join(proj_path, 'products/')
    
    #FILES
    post_launch_355= '/home/janmejoyarch/sftp_drive/suit_data/level1fits/2023/11/23/led355/SUT_UNP_9999_999999_Lev1.0_2023-11-23T08.00.31.908_A011BB03.fits'
    post_launch_255= '/home/janmejoyarch/sftp_drive/suit_data/level1fits/2023/11/23/led255/SUT_UNP_9999_999999_Lev1.0_2023-11-23T08.04.31.798_B011BB02.fits'
    baking_start_355= '/home/janmejoyarch/sftp_drive/suit_data/level1fits/2024/04/22/led355/SUT_T24_0701_000371_Lev1.0_2024-04-22T22.31.48.950_A011BB03.fits'
    baking_start_255= '/home/janmejoyarch/sftp_drive/suit_data/level1fits/2024/04/22/led255/SUT_T24_0701_000371_Lev1.0_2024-04-22T22.30.48.532_B011BB02.fits'
    post_baking_355= '/home/janmejoyarch/sftp_drive/suit_data/level1fits/2024/05/17/led355/SUT_C24_0302_000379_Lev1.0_2024-05-17T04.40.20.475_A011BB03.fits'
    post_baking_255= '/home/janmejoyarch/sftp_drive/suit_data/level1fits/2024/05/17/led255/SUT_C24_0302_000379_Lev1.0_2024-05-17T04.40.47.714_B011BB02.fits'
    now_355= '/home/janmejoyarch/sftp_drive/suit_data/level1fits/2024/07/09/led355/SUT_C24_0315_000460_Lev1.0_2024-07-09T05.30.21.532_A091BB03.fits' 
    now_255= '/home/janmejoyarch/sftp_drive/suit_data/level1fits/2024/07/09/led255/SUT_C24_0315_000460_Lev1.0_2024-07-09T05.30.48.762_B091BB02.fits'
    
    filelist=[post_launch_355,
            post_launch_255,
            baking_start_355,
            baking_start_255,
            post_baking_355,
            post_baking_255,
            now_355,
            now_255
                ]
    
    for file in filelist[2:]:
        hdu= fits.open(file)[0]
        print('-------------------------')
        print(os.path.basename(file))
        if hdu.header['LEDONOFF'].endswith('5500'): #355
            led_wl='355'; ref_img= os.path.basename(post_launch_355)
            print(led_wl)
            ref= fits.open(post_launch_355)[0].data
        elif hdu.header['LEDONOFF'].endswith('55'):
            led_wl='255'; ref_img= os.path.basename(post_launch_255)   
            print(led_wl)
            ref= fits.open(post_launch_255)[0].data
        data= hdu.data
        stats(data)
        
        #RATIO#
        filename_prefix= 'ratio_'
        ratio= data/ref
        hdu=fits.PrimaryHDU(ratio, header=prep_header(filename_prefix+os.path.basename(file), ref_img, led_wl, os.path.basename(file), 'DATA_IMG/REF_IMG --LED image Ratio'))
        if save==True: hdu.writeto(f'{sav}{filename_prefix}{os.path.basename(file)}', overwrite=True)
        print('-------------------------')
        
        ##NOISE##
        filename_prefix= 'noise_'
        noise_map= np.sqrt((1/data) + (1/ref))*ratio #see reference folder for error propagation.
        hdu=fits.PrimaryHDU(noise_map, header=prep_header(filename_prefix+os.path.basename(file), ref_img, led_wl, os.path.basename(file),'sig_X --Noise in (X)'))
        if save==True: hdu.writeto(f'{sav}{filename_prefix}{os.path.basename(file)}', overwrite=True)
        
        ##PLOTTING##
        if plot:
            plt.figure()
            plt.imshow(ratio, norm= colors.LogNorm(vmin= 0.3, vmax=2), origin='lower')
            plt.title(f'ratio_{os.path.basename(file)}')
            plt.colorbar()
            plt.show()
            
            plt.figure()
            plt.imshow(noise_map, norm= colors.LogNorm(), origin='lower')
            plt.title(f'noise_{os.path.basename(file)}')
            plt.colorbar()
            plt.show()