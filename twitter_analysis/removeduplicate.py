import time

import couchdb

start = time.time()
dic1 = {}
try:
    couchclient = couchdb.Server('http://admin:chocolate_milkshake@172.26.129.34:5984/')
except:
    print("Cannot connected to CouchDB Server\n")
    raise

try:
    db = couchclient['new_tweets']
    print("Connected to the user database")
except:
    db = couchclient['default']
    print("Connected to the default database")

duplicate_mango = {"selector": {},
                   "fields": ["_rev", "_id", "id", "createtime", "source", "text", "username", "userlocation",
                              "lang", "placename", "geo", "polarity", "subjectivity"], "limit": db.__len__()}

try:
    db2 = couchclient['no_duplicate_twitter']
    print("no_duplicate_twitter has already in the server!")
except couchdb.http.ResourceNotFound:
    db2 = couchclient.create('no_duplicate_twitter')
    print("Create no_duplicate_twitter in the server!")

print("Connected to the user database")


def save(database, mango):
    for items in database.find(mango):
        # print(items["_rev"])
        if items["_rev"] not in dic1.keys():
            dic1.update({items["_rev"]: items})
        else:
            continue
    # print(len(dic1))
    for items in dic1.values():
        db2.save(
            {"id": items["id"], "createtime": items["createtime"], "text": items["text"],
             "username": items["username"],
             "userlocation": items["userlocation"], "lang": items["lang"],
             "geo": items["geo"],
             "polarity": items["polarity"], "subjectivity": items["subjectivity"]})


if db2.__len__() == 0:
    try:
        couchclient.delete('lines_processed')
        couchclient.create('lines_processed')
    except:
        couchclient.create('lines_processed')
    db3 = couchclient['lines_processed']
    db3.save({"lines_processed": db.__len__()})
    save(db, duplicate_mango)


else:
    db3 = couchclient['lines_processed']
    lines_processedmango = {"selector": {}, "limit": db3.__len__()}
    for items in db3.find(lines_processedmango):
        lines_processed = (items["lines_processed"])
    if lines_processed != db.__len__():
        duplicate_mango2 = {"selector": {},
                            "fields": ["_rev", "_id", "id", "createtime", "text", "username", "userlocation",
                                       "lang", "geo", "polarity", "subjectivity"], "limit": db.__len__(),
                            "skip": lines_processed}
    save(db, duplicate_mango2)
    couchclient.delete('lines_processed')
    couchclient.create('lines_processed')
    db4 = couchclient['lines_processed']
    db4.save({"lines_processed": db.__len__()})

end = time.time()
print(end - start)