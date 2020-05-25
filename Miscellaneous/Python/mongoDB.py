#%%
from tinymongo import TinyMongoClient, TinyMongoCollection
data = [
    {'name': 'Peter', 'age': 20},
    {'name': 'Tom', 'age': 25},
    {'name': 'Pat', 'age':30},
]

client = TinyMongoClient('./testdb.db')
db = client['FirstDB']
collection: TinyMongoCollection = db['users']
collection.insert_many(data)

#%%
def query(d: dict):
    for x in collection.find(d):
        print(x)
    print("==== END ====")

#%%
query({'name': 'Peter'})

query({'name': {'$regex': 'P.*'}})

query(
    {'$or':
         [
             {'name': {'$regex': 'T.*'}},
             {'age': {'$gte': 25}}
         ]
    }
)

#%%
collection.find()