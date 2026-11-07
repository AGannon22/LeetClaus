import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

# Our own alfa-leetcode-api container. Docker sets this to http://leetcode-api:3000/.
leetcodeURL = os.getenv("LEETCODE_API_URL", "http://localhost:3000/")
def GETFROMXURL(url):
    try:
        response = requests.get(url,timeout=30)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None
def confirmLeetCodeUser(username):
    response = GETFROMXURL(leetcodeURL+username)
    if response is not None and 'errors' not in response:
        return True
    else:
        return False
