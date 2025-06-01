from dotenv import load_dotenv
import os

load_dotenv(override=True)

BASE_URL = os.environ["BASE_URL"]
EMAIL = os.environ["EMAIL"]
PASSWORD = os.environ["PASSWORD"]