#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 16:05:11 2019

@author: vladgriguta
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from astropy.io import fits









if __name__ == '__main__':
    f = fits.open('spectraFull/spec-0299-51671-0302.fits',mode='update')
    f[0].header
    print(f[0].data)
    f.flush()
    
    
    
    f[0].header['RA']
    f = fits.open('spectraFull/spec-0299-51671-0302.fits',mode='update')
    f[1].data['model']
    f[1].data['flux']
    int(f[0].header['SPEC_ID'])
    
    
    
    
    
    
    
    
    
    
    # spPlate-pppp-mmmmm.fits
