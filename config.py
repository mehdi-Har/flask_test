from pymongo import MongoClient
from urllib.parse import quote_plus

username = "randomstuffformehdi"
password = quote_plus("root")  
uri = f"mongodb+srv://{username}:{password}@cluster0.kkryhtz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(uri)
db = client["test_database"]
