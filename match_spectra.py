#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 17:59:30 2019

@author: vladgriguta
"""
import pandas as pd
import pickle

def save_obj(obj, name ):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    with open(name + '.pkl', 'rb') as f:
        return pd.DataFrame(pickle.load(f))
    
    

if __name__ == "__main__":
    filename = 'PhotometricIdentif/SciServerDownload/test_query_table_1000'
    data_table=load_obj(filename)
    
    data_table['objid']