from db import user_data

# One document per user in the user_data collection:
#   {"username": "alyssa",
#    "leetcode_username": "alyssa_lc",
#    "completed_days": [1, 2, 5],
#    "assigned": {"1": "two-sum", "2": "valid-parentheses"}}   # day number (as a string) -> problem slug


def newUserDataDoc(username, leetcodeUsername):
    # the starting document for a brand-new user (created at registration)
    return {
        "username": username,
        "leetcode_username": leetcodeUsername,
        "completed_days": [],
        "assigned": {},
    }


def getUserData(username):
    return user_data.find_one({"username": username})

def getCompletedDays(username):
    # set of day numbers this user has completed (empty if they haven't done any yet)
    doc = user_data.find_one({"username": username}, {"completed_days": 1})
    return set(doc.get("completed_days", [])) if doc else set()


def markDayCompleted(username, day):
    # $addToSet won't add a day twice; upsert creates the user's document the first time
    user_data.update_one(
        {"username": username},
        {"$addToSet": {"completed_days": day}},
        upsert=True,
    )
def unmarkDayCompleted(username, day):
    user_data.update_one({"username": username}, {"$pull": {"completed_days": day}})

def assignProblem(username, day, slug):
    # Mongo keys are strings, so day 3 is stored as "3"
    user_data.update_one({"username": username}, {"$set": {f"assigned.{day}": slug}})
