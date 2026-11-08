import os
import random
import requests
import json
from dotenv import load_dotenv

load_dotenv()
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
def getHomeStats(username):
    response = GETFROMXURL(leetcodeURL+username+'/profile')
    if response is None or 'errors' in response:
        return None
    return {
        "totalSolved": response["totalSolved"],
        "totalQuestions": response["totalQuestions"],
        "easySolved": response["easySolved"],
        "totalEasy": response["totalEasy"],
        "mediumSolved": response["mediumSolved"],
        "totalMedium": response["totalMedium"],
        "hardSolved": response["hardSolved"],
        "totalHard": response["totalHard"]
    }
def getRecentSubmissions(username):
    response = GETFROMXURL(leetcodeURL + username + '/acSubmission')
    if response is None or 'errors' in response:
        return None
    return response["submission"]
def solvedRecently(leetcodeUser, slug):
    recent = getRecentSubmissions(leetcodeUser)
    if recent is None:
        return None
    return any(s["titleSlug"] == slug for s in recent)
def pickAProblem(leetcodeUser, previousProblems, attempts=5):
    recent = getRecentSubmissions(leetcodeUser) or []
    excluded = set(previousProblems.values()) | {s["titleSlug"] for s in recent}
    for _ in range(attempts):
        skip = random.randint(0, 4000)
        response = GETFROMXURL(leetcodeURL + 'problems?limit=20&skip=' + str(skip))
        if response is None or 'errors' in response:
            return None
        for problem in response["problemsetQuestionList"]:
            if not problem["isPaidOnly"] and problem["titleSlug"] not in excluded:
                return problem
    return None