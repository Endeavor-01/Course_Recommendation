import pymongo

# Establish connection to the MongoDB server
client = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = client["datastore"]
mycol = mydb["users"]

# Function to insert a new user
def insert_user(username, password):
    user = {"username": username, "password": password}
    mycol.insert_one(user)

# Function to check if user exists
def check_user(username, password):
    query = {"username": username, "password": password}
    user = mycol.find_one(query)
    return user is not None

# Function to check if username exists
def username_exists(username):
    query = {"username": username}
    user = mycol.find_one(query)
    return user is not None
