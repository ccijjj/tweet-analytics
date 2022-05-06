import couchdb
import json

# It is generally accepted that if housing costs exceed 30% of a low-income household's gross income, the household is experiencing 
# housing stress (30/40 rule). That is, housing is unaffordable and housing costs consume a disproportionately high amount of household
# income. The RAI uses the 30 per cent of income rule. Rental affordability is calculated using the following equation, where 'qualifying 
# income' refers to the household income required to pay rent where rent is equal to 30% of income:
# 
# RAI = (Median income ∕ Qualifying Income) x 100
# 
# In the RAI, households who are paying 30% of income on rent have a score of 100, indicating that these households are at the critical 
# threshold for housing stress. A score of 100 or less indicates that households would pay more than 30% of income to access a rental 
# dwelling, meaning they are at risk of experiencing housing stress.
# 
# The RAI is a price index for housing rental markets. It is a clear and concise indicator of rental affordability relative to household 
# incomes, applied to geographic areas across Australia.

try:
    couchclient = couchdb.Server('http://admin:chocolate_milkshake@172.26.129.34:5984/')

    aurin_db_name = 'aurin_rental'
    
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

with open("rental.json",'r') as f:
    rent = json.load(f)

records = rent['features']

for record in records:
    doc = {}
    properties_list = record['properties']
    if properties_list['city'] == 'Greater Melbourne':
        if properties_list['rai_cityadjusted_3br_2014_q1'] or properties_list['rai_cityadjusted_3br_2014_q2'] or properties_list['rai_cityadjusted_3br_2014_q3'] or properties_list['rai_cityadjusted_3br_2014_q4']:
            rai_list = [properties_list['rai_cityadjusted_3br_2014_q1'],properties_list['rai_cityadjusted_3br_2014_q2'],properties_list['rai_cityadjusted_3br_2014_q3'],properties_list['rai_cityadjusted_3br_2014_q4']]
            rai_sum = 0
            rai_len = 0
            for i in rai_list:
                if i:
                    rai_sum += i
                    rai_len += 1
            average_rai = rai_sum/rai_len

            doc['Suburb code'] = properties_list['geography_name']
            doc['Average city rental affordability index'] = format(average_rai,'.2f')
            if average_rai>100:
                doc['Experiencing housing stess'] = True
            else:
                doc['Experiencing housing stess'] = False
            print(doc)
            aurin_db.save(doc)