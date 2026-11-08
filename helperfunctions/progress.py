from db import user_data

def newUserDataDoc(username, leetcodeUsername, prefDif):
    # the starting document for a brand-new user (created at registration)
    return {
        "username": username,
        "leetcode_username": leetcodeUsername,
        "completed_days": [],
        "assigned": {},
        "prefDifficulty": prefDif
    }

def getUserData(username):
    return user_data.find_one({"username": username})

def getCompletedDays(username):
    doc = user_data.find_one({"username": username}, {"completed_days": 1})
    return set(doc.get("completed_days", [])) if doc else set()


def markDayCompleted(username, day):
    user_data.update_one(
        {"username": username},
        {"$addToSet": {"completed_days": day}},
        upsert=True,
    )
def unmarkDayCompleted(username, day):
    user_data.update_one({"username": username}, {"$pull": {"completed_days": day}})

def assignProblem(username, day, slug):
    user_data.update_one({"username": username}, {"$set": {f"assigned.{day}": slug}})
