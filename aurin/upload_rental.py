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
    aurin_db_name = 'aurin_rent'

    # Check the duplication of database
    try:
        aurin_db = couchclient[aurin_db_name]
        print(aurin_db_name + " has already in the server!")
    except couchdb.http.ResourceNotFound:
        aurin_db = couchclient.create(aurin_db_name)
        print("Create " + aurin_db_name + " in the server!")
    print("Connected to the user database")

except:
    print("Cannot find CouchDB Server ... Exiting\n")
    print("----_Stack Trace_-----\n")
    raise

district = pd.read_csv('C:/Users/张澄钰/Desktop/CCC/project/australian_postcodes.csv')
for i in range(0, len(district)):
    code = district['SA4_CODE_2016'][i]
    name = district['SA4_NAME_2016'][i]
    postcode = district['postcode'][i]

    if postcode not in sa4code.keys():  # 只记录第一个位置
        sa4code[postcode] = code
        sa4name[postcode] = name

with open("C:/Users/张澄钰/Desktop/CCC/project/rent.json", 'r') as f:
    rent = json.load(f)

records = rent['features']

code = []
name = []
RAI = []
stress = []
for record in records:
    properties_list = record['properties']
    if properties_list['city'] == 'Greater Melbourne':
        if properties_list['rai_cityadjusted_3br_2014_q1'] or properties_list['rai_cityadjusted_3br_2014_q2'] or \
                properties_list['rai_cityadjusted_3br_2014_q3'] or properties_list['rai_cityadjusted_3br_2014_q4']:
            rai_list = [properties_list['rai_cityadjusted_3br_2014_q1'],
                        properties_list['rai_cityadjusted_3br_2014_q2'],
                        properties_list['rai_cityadjusted_3br_2014_q3'],
                        properties_list['rai_cityadjusted_3br_2014_q4']]
            rai_sum = 0
            rai_len = 0
            for i in rai_list:
                if i:
                    rai_sum += i
                    rai_len += 1
            average_rai = rai_sum / rai_len

            if int(properties_list['geography_name']) in sa4code.keys():
                code.append(sa4code[int(properties_list['geography_name'])])
                name.append(sa4name[int(properties_list['geography_name'])])

            RAI.append(float(format(average_rai, '.2f')))

rent = pd.DataFrame({'sa4code': code, 'sa4name': name, 'Average city rental affordability index': RAI})
rentgroup = rent.groupby(['sa4code', 'sa4name'], as_index=False)['Average city rental affordability index'].mean()
rentgroup

for i in range(0, len(rentgroup)):
    doc = {}
    doc['sa4code'] = rentgroup['sa4code'][i]
    doc['sa4name'] = rentgroup['sa4name'][i]
    doc['Average city rental affordability index'] = format(rentgroup['Average city rental affordability index'][i],
                                                            '.2f')
    if rentgroup['Average city rental affordability index'][i] > 100:
        doc['Experiencing housing stess'] = False
    else:
        doc['Experiencing housing stess'] = True
    print(doc)
    aurin_db.save(doc)