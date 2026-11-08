from db import user_data

# One document per user in the user_data collection:
#   {"username": "alyssa", "completed_days": [1, 2, 5]}

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
