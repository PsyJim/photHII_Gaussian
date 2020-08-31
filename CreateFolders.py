#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
photHII_Gaussian.py needs this function to work well. 

Created on Tue Jul 14 09:33:32 2020
@author: Jim Acosta
"""
import os

def CreateFolders(directories):
    for i in range(len(directories)):
        if not os.path.exists(os.getcwd() + directories[i]):
            os.makedirs(os.getcwd() + directories[i])
        else:
            pass

if __name__ == '__main__':
    directories = ['/casa']
    CreateFolders(directories)
