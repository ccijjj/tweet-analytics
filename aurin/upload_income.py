import couchdb
import json

try:
    couchclient = couchdb.Server('http://admin:chocolate_milkshake@172.26.129.34:5984/')

    aurin_db_name = 'aurin_income'
    
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

with open("income.json",'r') as f:
    income = json.load(f)

records = income['features']

for record in records:
    properties_list = record['properties']
    doc = {}
    doc['Area code'] = properties_list['sa4_code']
    doc['Area name'] = properties_list['sa4_name']
    
    doc['Median'] = properties_list['median_aud']
    doc['Mean'] = properties_list['mean_aud']
    doc['Sum'] = properties_list['sum_aud']
    doc['Earners median age'] = properties_list['median_age_of_earners_years']
    doc['Earners persons'] = properties_list['earners_persons']
    doc['Gini coefficient'] = properties_list['gini_coefficient_coef']
    
    print(doc)
    aurin_db.save(doc)