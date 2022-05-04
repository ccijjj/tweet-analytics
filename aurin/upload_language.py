import couchdb
import json

try:
    couchclient = couchdb.Server('')
    
    aurin_db_name = ''
    
    #Check the duplication of database
    try:
        aurin_db = couchclient[aurin_db_name]
        print(aurin_db_name + " has already in the server!")
    except couchdb.http.ResourceNotFound:
        tweet_db = couchclient.create(aurin_db_name)
        print("Create " + aurin_db_name +" in the server!")
    print("Connected to the user database")

except:
    print("Cannot find CouchDB Server ... Exiting\n")
    print("----_Stack Trace_-----\n")
    raise

with open("lang_spoken.json",'r') as f:
    lang_data = json.load(f)

with open("lang_spoken_meta.json",'r') as f:
    lang_meta = json.load(f)

records = lang_data['features']
selected_attributes = lang_meta['selectedAttributes']

language_name = ['English','Greek','Hindi','Indonesian','Italian','Japanese','Korean','Persian','Polish','Russian','Spanish','Thai','Turkish','Urdu','Vietnamese']
#language_code = {'English':'en','Greek':'el','Hindi':'hi','Indonesian':'id','Italian':'it','Japanese':'ja','Korean':'ko','Persian':'fa','Polish':'pl','Russian':'ru','Spanish':'es','Thai':'th','Turkish':'tr','Urdu':'ur','Vietnamese':'vi'}

for record in records:
    properties_list = record['properties']
    suburb = properties_list['sa3_name16']
    prop_name = []
    prop_num_list = []
    
    for key,value in properties_list.items():
        attributes = selected_attributes
        for i in range(len(attributes)):
            if key == attributes[i]['name']:
                prop_title = attributes[i]['title']
                if "And" not in prop_title and 'other' not in prop_title and 'Other' not in prop_title and 'not stated' not in prop_title and "Total" in prop_title:
                    prop_name.append(prop_title)
                    prop_num_list.append(value)
                break

    doc = {'suburb': suburb}
    
    lang_count = []
    total = 0
    for j in range(len(prop_name)):
        doc_split = prop_name[j].split(" ")
        for word in doc_split:
            if word in language_name:
                lang_name = word
                lang_count.append((lang_name,prop_num_list[j]))
                total += prop_num_list[j]
                break
    doc['Language Count'] = sorted(lang_count, key = lambda count:count[1], reverse = True)
    doc['Total Count'] = total
    print(doc)
    aurin_db.save(doc)