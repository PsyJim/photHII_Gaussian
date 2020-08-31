#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auxiliary function for HIIGaussian_Jim FITS plotting.

Created on Wed Aug  5 20:16:05 2020
@author: jim
"""
from matplotlib import pyplot as plt
from mpdaf.obj import Image
import numpy as np
import os

#Define name of galaxy and directory for output images
OUTPUT_IMAGES_PATH = (os.getcwd() + '/IMAGES/')
name = 'NGC3614'

#Define filename of galaxy FITS
filename = (os.getcwd() + '/DATA/N3614p_calib_rot_rec.fits')

#Opening FITS data
ima = Image(filename)
#Positive data for better plotting
ima.data[ima.data < 0] = 0

#FITS directories
directories = ['3_flux_min','5_flux_min','7_flux_min','10_flux_min','xav_flux_min',]
ID = ['3_fm','5_fm','7_fm','10_fm','xav_fm']

for i in range(len(directories)):
    #Opening FITS data for gaussian and diffuse regions
    gfitim = Image(os.getcwd() + '/' + name + '/' + directories[i]  + '/N3614p_gfitim_' + ID[i] + '.fits')
    gfitim2 = Image(os.getcwd() + '/' + name + '/' + directories[i]  + '/N3614p_gfitim2_' + ID[i] + '.fits')
    grid = Image(os.getcwd() + '/' + name + '/' + directories[i]  + '/N3614p_grid_' + ID[i] + '.fits')
    res2 = Image(os.getcwd() + '/' + name + '/' + directories[i]  + '/N3614p_res2_' + ID[i] + '.fits')

    #Obtaining values such as gaussian regions quantity and min flux from table 
    table = np.genfromtxt(os.getcwd() + '/' + name + '/' + directories[i] + '/data_N3614p_' + ID[i] + '.csv', delimiter = ',', skip_header=0)
    alpha, chi2_global, F_min = float(table[0]), float(table[1]), float(table[2])
    
    #Plotting figure
    fig, ax = plt.subplots(2, 3, figsize=(12,8))
    fig.suptitle('# {} HII regions - Chi2 {}'.format(alpha,np.round(chi2_global,2)), fontsize=16)

    ima.plot(scale='log', colorbar='v', ax=ax[0,0], vmin=0, vmax=0.9*np.amax(ima.data), zscale=False, title=r'flux = %s [10$^{-16}$ cgs]'%( np.round(np.sum(ima.data),2)))
    #ax[0,1].scatter(IPd,JPd, color='red', marker='.', linewidth=0.01)
    gfitim.plot(scale='log', vmin=0, vmax=0.9*np.amax(gfitim.data), colorbar='v', ax=ax[0,1],   zscale=False, title=r'flux = %s [10$^{-16}$ cgs]'%( np.round(np.sum(gfitim.data),2)))
    gfitim2.plot(scale='log', vmin=0, vmax=0.9*np.amax(gfitim2.data), colorbar='v', ax=ax[0,2],   zscale=False, title=r'flux = %s [10$^{-16}$ cgs]'%( np.round(np.sum(gfitim2.data),2)))
    grid.plot(scale='log', vmin=0, vmax=0.9*np.amax(grid.data), colorbar='v', ax=ax[1,0],   zscale=False, title=r'flux = %s [10$^{-16}$ cgs]'%( np.round(np.sum(grid.data),2)))

    res2.plot(vmin=-3*F_min, vmax=3*F_min, colorbar='v', ax=ax[1,1],   zscale=False, title=r'flux = %s [10$^{-16}$ cgs]'%( np.round(np.sum(res2.data),2)))

    res2.data[res2.data < 0] = 0
    res2.plot(scale='log', vmin=0, vmax=0.9*np.amax(res2.data), colorbar='v', ax=ax[1,2],   zscale=False, title='mean = {}, median = {}, std = {}'.format(np.round(np.mean(np.ravel(res2.data)),3), np.round(np.median(np.ravel(res2.data)),3), np.round(np.std(np.ravel(res2.data)),3)))
    fig.tight_layout()

    # Save plotting in pdf and png
    #fig.savefig(OUTPUT_IMAGES_PATH + 'HII_recover_{}.pdf'.format(name), bbox_inches='tight', transparent=True)
    #fig.savefig(OUTPUT_IMAGES_PATH + 'HII_recover_{}.png'.format(name), bbox_inches='tight', transparent=True)

    plt.show()
    #plt.close()
