#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 12:16:58 2019

@author: vladgriguta

Downloads the spectra of the objects in a multi-threading manner, allowing
for fast download of data.

"""
import numpy as np
import os
import datetime
NUM_CPUS = 4  # defaults to all available

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
    return addresses, i

def worker(address,nothing):
    os.system("wget "+address)

def test_run(pool,addresses,not_successful):
    nothing=True
    for i in range(len(addresses)):
        for j in range(len(addresses[i])):
            try:
                pool.apply_async(worker, args=(addresses[i][j],nothing))
            except:
                print("The address number "+str(j)+" from stack "+str(i)+"was not downloaded")
                not_successful.extend((i,j))
                
        #pool.apply_async(worker, args=(add[0],nothing))
            
if __name__ == "__main__":
    import multiprocessing as mp
    pool = mp.Pool(NUM_CPUS)
     
    
    initialTime = datetime.datetime.now()
    
    addresses,n_addresses = get_address_lists(4)
    not_successful = []
    test_run(pool,addresses,not_successful)
    pool.close()
    pool.join()
    
    duration = datetime.datetime.now()-initialTime

    print("The download of "+str(n_addresses)+" addresses took "+str(duration))
    
    # Save array of data that was not downloaded properly
    not_successful = np.array(not_successful)
    np.savetxt('../unsuccessfull.txt',not_successful,dtype=int)
    
    



