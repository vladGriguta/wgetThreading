#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 12:16:58 2019

@author: vladgriguta

Downloads the spectra of the objects in a multi-threading manner, allowing
for fast download of data.

"""
import os
NUM_CPUS = 2  # defaults to all available

def get_address_lists(n_lists,file='../download_url.txt'):
    addresses = []
    for i in range(n_lists):
        addresses.append([])
    with open(file,'r') as txt_file:
        content = txt_file.readlines()
        # round to higher integer
        n_elem = int(len(content)/n_lists) + (len(content) % n_lists > 0)
        for i in range(len(content)):
            addresses[int(i/n_elem)].append(content[i])
    return addresses

def worker(address_list,directory):
    os.system("wget "+address_list+" "+directory)

def test_run(pool,addresses,directory):
    for add in addresses:
        for i in range(len(add)):
            pool.apply_async(worker, args=(add[i],directory))
        
        #pool.apply_async(worker, args=(add[0],directory))

if __name__ == "__main__":
    import multiprocessing as mp
    pool = mp.Pool(NUM_CPUS)
     
    directory = 'spectraFull/'
     
    addresses = get_address_lists(4)
    
    test_run(pool,addresses,directory)
    pool.close()
    pool.join()



