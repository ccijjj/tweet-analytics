import couchdb
import json

try:
    couchclient = couchdb.Server('http://admin:chocolate_milkshake@172.26.129.34:5984/')

    aurin_db_name = 'aurin_unemployment'
    
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

def create_unemployment_doc(unemployment):
    
    records = unemployment['features']
    doc_list = []

    for record in records:
        properties_list = record['properties']
        
        area_code = properties_list['sa4_code']
        area_name = properties_list['sa4_name']
        unemployed_total = float(format(properties_list['unemployed_tot_000'],'.3f'))*1000
        avg_job_search_wks = properties_list['avg_duration_job_search_wks']

        doc = [area_code,area_name,unemployed_total,avg_job_search_wks]
        doc_list.append(doc)
    
    return doc_list

def combine_list(total_list, list):
    for doc1 in total_list:
        for doc2 in list:
            if doc1[0] == doc2[0]:
                doc1.append(doc2[2])
                doc1.append(doc2[3])
    return total_list

with open("unemployment2014.json",'r') as f:
    unemployment14 = json.load(f)

with open("unemployment2015.json",'r') as f:
    unemployment15 = json.load(f)

with open("unemployment2016.json",'r') as f:
    unemployment16 = json.load(f)

with open("unemployment2017.json",'r') as f:
    unemployment17 = json.load(f)

list_14 = create_unemployment_doc(unemployment14)
list_15 = create_unemployment_doc(unemployment15)
list_16 = create_unemployment_doc(unemployment16)
list_17 = create_unemployment_doc(unemployment17)

total_list = list_14
total_list = combine_list(total_list, list_15)
total_list = combine_list(total_list, list_16)
total_list = combine_list(total_list, list_17)

doc_keys = ['Area name', 'Area code', 'Unemployed total in 2014','Average duration of job search in 2014','Unemployed total in 2015','Average duration of job search in 2015','Unemployed total in 2016','Average duration of job search in 2016','Unemployed total in 2017',
'Average duration of job search in 2017']

for item in total_list:
    doc_values = item
    doc = dict(zip(doc_keys,doc_values))
    
    print(doc)
    aurin_db.save(doc)