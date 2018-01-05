# -*- coding: utf-8 -*-
"""
Modified on January 05, 2018

@author: kerni016
"""
import json
import csv
import urllib
import os.path

######################################

### Manual items to change!

ActionDate = '20180105'

## name of the main directory containing the script and the json file
directory = r'C:\BTAA\Maintenance\DKANtest'

localJson = directory + '\data.json'
csvfile =  directory + '\DistributionFile_%s.csv' % (ActionDate)


#######################################

### opens local json file and loads to a dictionary
with open(localJson) as data_file:
	newdata = json.load(data_file)

### prints a list of the distribution formats for the resources in the portal
distribution_format = []
default = 'None'

for y in range(len(newdata["dataset"])):
    distribution = newdata["dataset"][y]['distribution']
    for x in distribution:
       distribution_format.append(x.get('format', default))
distribution_set = set(distribution_format)

print distribution_set
        
###compare this to a library of distribution formats we have seen before?

###Dictionary to store information about distribution for each resource identifier
DistributionDict ={}

###Types of distributions of interest to the geoportal project
downloadable = ['shp','gdb','fgdb','LAS']
webservice = ['esri rest', 'rest']

  
for y in range(len(newdata["dataset"])):
    distribution = newdata["dataset"][y]['distribution']
    identifier = newdata["dataset"][y]["identifier"]
    
    ###For each resource in the portal, counts how many distributions of each type are available.  If there is no "format" listed, it is counted as unknown.
    count_data = 0
    count_webservice = 0
    count_metadata = 0
    count_other = 0
    count_unknown = 0
    metadata = []
    for x in distribution:        
        try:
            if x['format'] in downloadable:
                count_data += 1
            elif x['format'] in webservice:
                count_webservice += 1
            elif x['format'] == 'metadata':
                count_metadata += 1
            else:
                count_other += 1
        except:
            count_unknown += 1
    #print count_data, count_webservice, count_metadata, count_other, count_unknown
    
    ###If there is only one distribution for a resource labeled downloadable, web service, or metadata, adds the download/access URL to information about the identifier. If there are more than one distribution of that type it adds "multiple" and if there are no resources of that type, it adds "none".
    try:
        if count_data == 1:
            for x in distribution:
                if x['format'] in downloadable: 
                    try:
                        metadata.append(x['accessURL'])
                    except:
                        metadata.append(x['downloadURL'])
        elif count_data > 1:
            metadata.append('multiple')
        else:
            metadata.append('none')
        if count_webservice == 1:
            for x in distribution:
                if x['format'] in webservice:            
                    metadata.append(x['accessURL'])
        elif count_webservice > 1:
            metadata.append('multiple')
        else:
            metadata.append('none')
        if count_metadata == 1:
            for x in distribution:
                if x['format'] == 'metadata':
                    metadata.append(x['accessURL'])
        elif count_metadata > 1:
            metadata.append('multiple')
        else:
            metadata.append('none')    
        ### Adds to the metadata the number of other distribution formats and distributions for which there is no format information  
        metadata.append(count_other)
        metadata.append(count_unknown)
    ###If the above script returns an error, a warning is printed
    except:
        print "error :" + identifier
    ###The information about the distributions is added to the dictionary for each key identifier
    DistributionDict[identifier] = metadata

### Information printed to a csv
with open(csvfile, 'wb') as outfile:
    csvout = csv.writer(outfile)
    csvout.writerow(["downloadable","web_service", "metadata", "other", "unknown", "id"])
    for keys in DistributionDict:
        allvalues = DistributionDict[keys]
        allvalues.append(keys)
        csvout.writerow(allvalues)
    
      
#known types:
#set([u'shp', u'raster', 'None', u'rest', u'application', u'gdb', u'portal', u'fgdb', u'LAS', u'data', u'esri rest', u'metadata'])

#key, value in x.iteritems() :
            #print distribution[x]['format']
            #print key
            #stuff = x
        #distribution_format.append(stuff['format'])

#if in x.iteritems, key format exists and it = item in downloadable list:
    #add to temporary list
#count each list 
    #if no objects metadata.append('none')
    #if multiple objects metadata.append('multiple'+ leng(temp_list))
    #if one relevant object iterate back through and add accessURL or downloadURL
#else add other type to a list