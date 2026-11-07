import requests

leetcodeURL = "https://alfa-leetcode-api.onrender.com/"
def confirmLeetCodeUser(username):
    try:
        response = requests.get(leetcodeURL + username)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None