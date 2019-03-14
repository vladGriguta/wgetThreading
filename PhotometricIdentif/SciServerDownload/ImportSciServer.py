# -*- coding: utf-8 -*-
"""
Created on Mon Feb  4 20:40:14 2019

@author: Robin
"""

from SciServer import Authentication, LoginPortal, Config, CasJobs, SkyQuery, SciDrive
import numpy as np
import pickle

def save_obj(obj, name ):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)

#You need to create a SciServer account
Authentication_loginName = 'Robing';
Authentication_loginPassword = 'mphysproject'
token = Authentication.login(Authentication_loginName, Authentication_loginPassword);

#FIRST match query - perhaps input as separate text file later on?
#This webapge is good to check your SQL syntax if you're having problems: http://skyserver.sdss.org/dr13/en/tools/search/form/searchform.aspx

query="""
SELECT top 1000 sp.ra,sp.dec,sp.z,sp.class,sp.subclass,sp.objid,
sp.psfmag_u-sp.extinction_u AS mag_u,
sp.psfmag_g-sp.extinction_g AS mag_g,
sp.psfmag_r-sp.extinction_r AS mag_r,
sp.psfmag_i-sp.extinction_i AS mag_i,
sp.psfmag_z-sp.extinction_z AS mag_z,
w.w1mpro AS w1,
w.w2mpro AS w2,
w.w3mpro AS w3,
w.w4mpro AS w4,
f.peak,f.integr,f.rms
FROM SpecPhoto AS sp
JOIN wise_xmatch AS xm ON sp.objid = xm.sdss_objid
JOIN FIRST AS f ON sp.objid = f.objid
JOIN wise_allsky AS w ON xm.wise_cntr = w.cntr
WHERE
(sp.psfmag_r-sp.extinction_r > 0)
"""

#quick synchronous job - probably isn't what you want for any meaningful runs:
#queryResponse = CasJobs.executeQuery(query, "dr14", format='pandas')
#gals = queryResponse

#check tables in myDB
tname='test'
data=CasJobs.getTables('MyDB')
if data:
    print(data)
    print('There are already tables in your database under that name, removing them before doing new query...')
    #CLEAN UP: delete table from myDB
    SkyQuery.dropTable(tableName=tname, datasetName='myDB')

#long asynchronous job
print('submitting SQL job to SciServer... could take some time depending on query length and SciServer load...')
jobID = CasJobs.submitJob(query+ "into myDB."+tname, "dr14")
CasJobs.waitForJob(jobID, verbose=True)

try:
    #Download table from MYDB into Pandas dataframe. additional parms: , top=10
    print('Attempting to download table...')
    data_table = SkyQuery.getTable(tableName=tname, datasetName='MyDB')
    print('Done! Table shape is: '+str(data_table.shape))
    #save df to disk in case of super long queries:
    filename='test_query_table_1000'
    print('Saving tables to disk as: '+filename)
    save_obj(data_table, filename)
except:
    print('ERROR, No data found in your SciServer database, query may not have completed, check your SQL syntax?')
    #see tables in MyDB
    tables = SkyQuery.listDatasetTables('MyDB')
    print('tables found: ', tables)

#CLEAN UP: delete table from myDB
SkyQuery.dropTable(tableName=tname, datasetName='MyDB')
#Check tables are gone from MyDB
#tables = SkyQuery.listDatasetTables('MyDB')
#print('tables in MyDB (should be none?): '+str(tables))








