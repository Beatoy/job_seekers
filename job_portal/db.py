from pymongo import MongoClient

def get_db():
    client = MongoClient('mongodb+srv://dilan:1234@cluster0.sr8rhz4.mongodb.net/?appName=Cluster0')
    db = client['job_portal']
    return db
