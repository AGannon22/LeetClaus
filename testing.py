import requests
leetcodeURL = "https://alfa-leetcode-api.onrender.com/dunkdunkle"
def main():
    try:
        response = requests.get(leetcodeURL)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None
if __name__ == '__main__':
    print(main())