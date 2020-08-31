#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auxiliary function that calculate the integrated flux for circular and
eliptical apertures.

Created on Wed Jul 29 20:53:43 2020
@author: Jim Acosta
"""
from photutils import CircularAperture, EllipticalAperture
from photutils import aperture_photometry
from matplotlib import pyplot as plt
from mpdaf.obj import Image #remember install this python package
import numpy as np
import os


def circle_aperture_pix(filename, position, r_end = 7, plot = True):
    #Opening FITS, getting data and header
    ima = Image(os.getcwd() + '/DATA/' + filename + '.fits')
    hdr = ima.data_header
    data = ima.data.copy()
    
    #Galaxy center position and position for apertures
    center = (hdr['CRPIX1'], hdr['CRPIX2'])
    position = position + center

    #Defining radius for circular apertures
    radius = 50*np.arange(1, r_end)
    aperture = [CircularAperture(position, r = i) for i in radius]

    if plot == True:
        #Plot galaxy image with apertures
        fig, ax = plt.subplots()
        ima.data[ima.data < 0] = 0
        
        ima.plot(ax, scale = 'log', vmin = 0, vmax = 0.9*np.amax(ima.data), colorbar = 'v')        
        for i in range(len(aperture)):
            aperture[i].plot(ax, color = 'white', lw = 2)
        ax.set_title(r'Original image - NGC 3614')
        #plt.savefig('Image_apertures', dpi = 200)

    #Table with apertures data (flux sum)
    phot_table = aperture_photometry(data, aperture)
    for col in phot_table.colnames:
        phot_table[col].info.format = '%.8g'
    print(phot_table)
    
    return data, position, aperture


def elliptic_aperture_pix(filename, position, ellipticity, theta, r_end = 9, plot = True):
    #Opening FITS, getting data and header
    ima = Image(os.getcwd() + '/DATA/' + filename + '.fits')
    hdr = ima.data_header
    data = ima.data.copy()

    #Galaxy center position and position for apertures
    center = (hdr['CRPIX1'], hdr['CRPIX2'])
    position = position + center

    #Defining radius for circular apertures
    radius = 50*np.arange(1, r_end)
    aperture = [EllipticalAperture(position, i, i*ellipticity, theta) for i in radius]

    if plot == True:
        #Plot galaxy image with apertures
        fig, ax = plt.subplots(sharex=True,sharey=True)
        ima.data[ima.data < 0] = 0
        
        ima.plot(ax, scale = 'log', vmin = 0, vmax = 0.9*np.amax(ima.data), colorbar = 'v')      
        for i in range(len(aperture)):
            aperture[i].plot(ax, color = 'white', lw = 2)
        ax.set_title(r'Original image - NGC 3614')            
        #plt.savefig('Image_apertures', dpi = 200)

    #Table with apertures data (flux sum)
    phot_table = aperture_photometry(data, aperture)
    for col in phot_table.colnames:
        phot_table[col].info.format = '%.8g'
    print(phot_table)
 
    return data, position, aperture


def flux_vs_radius(data, aperture, r_end = 7):
    #Plot galaxy flux vs aperture radius
    plt.figure()
    plt.title(r'Flux vs Radius - NGC 3614')
    plt.ylabel(r'Flux [idk]')
    plt.xlabel(r'Radius [pixels]')
    
    radius = 50*np.arange(1, r_end)
    
    phot_table = aperture_photometry(data, aperture)
    #for col in phot_table.colnames:
    #    phot_table[col].info.format = '%.8g'
    #print(phot_table)

    #Integrating flux apertures
    aperture_sum = np.zeros(len(radius))
    for i in range(0, len(radius)):
        aperture_sum[i] = (phot_table['aperture_sum_' + str(i)][0])

    #Plotting flux vs aperture radius
    plt.plot(radius, aperture_sum, color = 'black')
    plt.savefig('flux_vs_radius', dpi = 200)
    return aperture_sum
    

def circlemask(shape, center, radius):
    #Arrays with x & y shapes. x & y changed.
    y,x = np.ogrid[:shape[0],:shape[1]] 
    cx,cy = center
    
    #Calculating r of desired circle
    r = np.sqrt(((x-cx)**2) + ((y-cy)**2)) 
    circmask = (r <= radius)
    return circmask


def std_prom(data, aperture, position):
    std = []
    data_no_masked = data.copy()
    for i in range(len(position[:,0])):
        data = data_no_masked.copy()
        mask = circlemask(data.shape, position[i], aperture[0].r)
        data[~mask] = None #Convert data out mask to NaNs
        data = np.ma.masked_invalid(data) #Mask invalid data like NaNs to --
        std.append(np.std(data)) 
        std_prom = sum(std)/len(position)
        print('\nStandart deviation position +' + '['+i+']' +  '= ', std[i])
    print('\nStandart deviation prom = ', std_prom)
    return std_prom


if __name__ == '__main__':
    #Recover data, position and aperture from aperture_pix function
    #FITS filename
    filename = 'N3614p_calib_rot_rec'
    #points = np.array([[-302,-398],[-610,401],[332,380]]) #points defined from center
    points = np.array([0,0])
    ellipticity = 0.40
    theta = 101*180/np.pi
    data, position, aperture = circle_aperture_pix(filename, points)
    data, position, aperture = elliptic_aperture_pix(filename, points, ellipticity, theta)

    #Normalization keyword for Histogramic scale plotting
    #norm = ImageNormalize(vmin = np.amin(data), vmax = np.amax(data),
    #                      stretch=LogStretch(data))


    #Appling circle mask to data
    #mask = circlemask(data.shape, position, aperture[7].r)
    #data[mask] = None #Convert data in mask to NaNs
    #data[~mask] = None #Convert data out mask to NaNs
    #data = np.ma.masked_invalid(data) #Mask invalid data like NaNs to --


    #Plotting masked data
    #plt.figure()
    #plt.title(r'10% flux - NGC 3614')
    #plt.imshow(data, norm=norm, cmap='viridis', origin='lower')
    #plt.colorbar(label=r'(H$_\alpha$)')
    #plt.savefig('10%_flux', dpi = 200)
