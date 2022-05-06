import couchdb
import json

try:
    couchclient = couchdb.Server('http://admin:chocolate_milkshake@172.26.129.34:5984/')

    aurin_db_name = 'aurin_life'
    
    #Check the duplication of database
    try:
        aurin_db = couchclient[aurin_db_name]
        print(aurin_db_name + " has already in the server!")
    except couchdb.http.ResourceNotFound:
        aurin_db = couchclient.create(aurin_db_name)
        print("Create " + aurin_db_name +" in the server!")
    print("Connected to the user database")

except:
    print("Cannot find CouchDB Server ... Exiting\n")
    print("----_Stack Trace_-----\n")
    raise

with open("life.json",'r') as f:
    life = json.load(f)

records = life['features']

for record in records:
    properties_list = record['properties']
    
    doc = {}
    doc['Area code'] = properties_list['sa4_code16']
    doc['Area name'] = properties_list['sa4_name16']

    doc['Male life expectancy(2013-15)'] = properties_list['life_expectancy_m_2013_15']
    doc['Male life expectancy(2014-16)'] = properties_list['life_expectancy_m_2014_16']
    doc['Male life expectancy(2015-17)'] = properties_list['life_expectancy_m_2015_17']
    doc['Male life expectancy(2016-18)'] = properties_list['life_expectancy_m_2016_18']
    doc['Male life expectancy(2017-19)'] = properties_list['life_expectancy_m_2017_19']
    
    doc['Female life expectancy(2013_15)'] = properties_list['life_expectancy_f_2013_15']
    doc['Female life expectancy(2014-16)'] = properties_list['life_expectancy_f_2014_16']
    doc['Female life expectancy(2015-17)'] = properties_list['life_expectancy_f_2015_17']
    doc['Female life expectancy(2016-18)'] = properties_list['life_expectancy_f_2016_18']
    doc['Female life expectancy(2017-19)'] = properties_list['life_expectancy_f_2017_19']

    doc['Person life expectancy(2013_15)'] = properties_list['life_expectancy_p_2013_15']
    doc['Person life expectancy(2014-16)'] = properties_list['life_expectancy_p_2014_16']
    doc['Person life expectancy(2015-17)'] = properties_list['life_expectancy_p_2015_17']
    doc['Person life expectancy(2016-18)'] = properties_list['life_expectancy_p_2016_18']
    doc['Person life expectancy(2017-19)'] = properties_list['life_expectancy_p_2017_19']

    print(doc)
    aurin_db.save(doc)