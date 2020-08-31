#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
photHII_Gaussian.py needs this function to work well. 

Created on Thu Aug 13 23:43:32 2020
@author: Jim Acosta
"""
#import os

def CreateTable(name, directory, data):
    with open(directory + 'data_{}.csv'.format(name),'w') as file:
        for i in range(len(data)):
            file.write(str(data[i]) + ', ')
        file.close()

#if __name__ == '__main__':
#    name = 'intento'
#    directory = os.getcwd() + '/'
#    data = [1,'b','c']
        
#    CreateTable(name, data)
