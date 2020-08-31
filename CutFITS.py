#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auxiliary function to cut FITS into a smaller region.

Created on Thu Jun 27 16:42:29 2019
@author: Camila Angulo
"""
#import numpy as np
from mpdaf.obj import Image
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from astropy.io import fits
from astropy.coordinates import SkyCoord
from astropy.wcs import WCS
from astropy.nddata import Cutout2D
import astropy.units as u
import os


#Leer lista de coordenadas
#archivo=pd.read_csv('20coords.csv')
#coords=[]    
#archivo = open('coords.csv')
#for line in archivo:
#    line=line.replace(',',' ') 
#    line=line.replace('\n','')
#    if line != '':
#        coords.extend([line])
#coords=np.array(coords)
#x=np.arange(coords.size)



#Read list of coordinates and filenames
#filenames=[]    
#Archivo = open('fits_filename_data.csv')
#for line in Archivo:
#    line=line.replace('\n','')
#    if line != '':
#        filenames.extend([line])
#filenames=np.array(filenames)
#print(pd.isna(filenames))


def cut_save(filename, position, size):
    #Load image for data and wht, also wcs
    hdu = fits.open(os.getcwd() + '/DATA/' + filename)
    hdr = hdu[0].header
    data = hdu[0].data  
    wcs_data = WCS(hdr)
   
    try:
        #Make the cutout, including the wcs
        cutout_data = Cutout2D(data, position=position, size=size, wcs = wcs_data)
        hdu[0].data = cutout_data
    
        #Plotting cutout image
        plt.imshow(cutout_data, origin='lower', cmap='v', norm=LogNorm())
        plt.show()
    
        #Update header with the cutout WCS
        data.header.update(cutout_data.wcs.to_header())
    
        #Write the cutout to a new FITS file
        cutout_filename = 'cut_'+filename
        hdu.writeto(os.getcwd() + '/DATA/' + cutout_filename, overwrite=True)

    except:    
        ima = Image(os.getcwd() + '/DATA/' + filename)
        x_1, x_2 = hdr['CRPIX1'] - size[0], hdr['CRPIX2'] + size[0]
        y_1, y_2 = hdr['CRPIX1'] - size[1], hdr['CRPIX2'] + size[1]
        ima_cut = Image.copy(ima[x_1:x_2,y_1:y_2])
        hdu[0].data = ima_cut.data
        
        #Plotting cutout image
        plt.imshow(ima_cut.data, origin='lower', cmap='viridis', norm=LogNorm())
        plt.show()
   
        #Write the cutout to a new FITS file
        cutout_filename = 'cut_'+filename
        hdu.writeto(os.getcwd() + '/DATA/' + cutout_filename, overwrite=True)
    
    hdu.close()
    
    
    

#Go through the files to cut the FITS files
#for i in x:   
filename = 'N5406p_calib_rot.fits'       
#size = u.Quantity((1, 1), u.arcmin) #Size of the cutout image
size = [800, 800]
position = SkyCoord(210.0838228433923, 38.91548699748973, frame='icrs', unit = u.deg)
#position = (hdr['CRVAL1'], hdr['CRVAL2'])
cut_save(filename, position, size) 



