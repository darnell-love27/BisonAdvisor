from pymongo import MongoClient

def get_database():
    # Replace the connection string with your MongoDB Atlas connection string
    CONNECTION_STRING = "mongodb+srv://<username>:<password>@cluster0.gplhetr.mongodb.net/?retryWrites=true&w=majority"

    try:
        # Create a MongoClient using the provided connection string
        client = MongoClient(CONNECTION_STRING)
        # Access your specific database
        db = client['BisonAdvisor']
        return db
    except Exception as e:
        # Handle connection errors
        print(f"Connection to MongoDB failed: {e}")
        return None
