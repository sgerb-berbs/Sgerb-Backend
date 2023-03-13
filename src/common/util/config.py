# Load enviornment variables
from dotenv import load_dotenv
load_dotenv()


# Set config data
import os
db_uri = os.getenv("DB_URI", "mongodb://127.0.0.1:27017")
db_name = os.getenv("DB_NAME", "sgerb")
