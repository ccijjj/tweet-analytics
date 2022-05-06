import couchdb
import json

try:
    couchclient = couchdb.Server('http://admin:chocolate_milkshake@172.26.129.34:5984/')

    aurin_db_name = 'aurin_language'
    
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


def creat_language_doc(lang, lang_meta):
    records = lang['features']
    selected_attributes = lang_meta['selectedAttributes']
    
    doc_list = []
    for record in records:
        properties_list = record['properties']
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

        doc = {}
        doc['Area code'] = properties_list['sa4_code16']
        doc['Area name'] = properties_list['sa4_name16']

        lang_count = []
        total = 0
        for j in range(len(prop_name)):
            doc_split = prop_name[j].split(" ")
            for word in doc_split:
                if word in language_name:
                    lang_name = word
                    #doc[lang_name] = prop_num_list[j]
                    lang_count.append((lang_name,prop_num_list[j]))
                    total += prop_num_list[j]
                    break
        doc['Language Count'] = lang_count
        doc['Total Count'] = total
        doc_list.append(doc)
    
    return(doc_list)



with open("lang1.json",'r') as f:
    lang1 = json.load(f)

with open("lang2.json",'r') as f:
    lang2 = json.load(f)

with open("lang1meta.json",'r') as f:
    lang1meta = json.load(f)

with open("lang2meta.json",'r') as f:
    lang2meta = json.load(f)

language_name = ['Arabic','Chinese','Dutch','English','French','German','Greek','Hindi','Indonesian','Italian','Japanese','Korean','Persian','Polish','Russian','Spanish','Thai','Turkish','Urdu','Vietnamese']

doc_list1 = creat_language_doc(lang1, lang1meta)
doc_list2 = creat_language_doc(lang2, lang2meta)

for doc in doc_list1:
    new_count_list = []
    cl_total = 0
    for count in doc['Language Count']:
        if count[0] == 'Chinese':
            cl_total += count[1]
        else:
            new_count_list.append(count)
    new_count_list.append(('Chinese', cl_total))
    doc['Language Count'] = new_count_list 

final_doc_list = doc_list1

for doc1 in final_doc_list:
    for doc2 in doc_list2:
        if doc1['Area code'] == doc2['Area code']:
            final_lang_count = doc1['Language Count'].copy()
            total = doc1['Total Count']
            for count in doc2['Language Count']:
                if count not in doc1['Language Count']:
                    final_lang_count.append(count)
                    total += count[1]
            doc1['Language Count'] = (sorted(final_lang_count, key = lambda count:count[1], reverse = True))
            doc1['Total Count'] = total
            print(doc1)
            aurin_db.save(doc1)