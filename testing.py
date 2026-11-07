import requests
from helperfunctions.leetcodeAPI import confirmLeetCodeUser
leetcodeURL = "https://alfa-leetcode-api.onrender.com/"
def main():
    try:
        response = requests.get(leetcodeURL)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None
def testingNotRealUser(user):
    try:
        response = requests.get(leetcodeURL + user)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None
if __name__ == '__main__':
    print(testingNotRealUser("GNOEGGHJDFHGFJDKJFHJDKDJFHGJKFJGHJKGJH"))