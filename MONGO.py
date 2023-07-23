import os
from pymongo.mongo_client import MongoClient
from urllib.parse import quote_plus
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()


class MONGO:

    def get_mongo_client(self):

        # Read the MongoDB username and password from environment variables
        username = os.environ.get("MONGODB_USERNAME")
        password = os.environ.get("MONGODB_PASSWORD")

        # Escape the username and password using quote_plus()
        escaped_username = quote_plus(username)
        escaped_password = quote_plus(password)

        # Construct the MongoDB URI with the escaped username and password
        mongo_uri = f"mongodb+srv://{escaped_username}:{escaped_password}@cluster0.wx4mi.mongodb.net/?retryWrites=true&w=majority"

        # Establish a connection to MongoDB
        client = MongoClient(mongo_uri)
        return client
