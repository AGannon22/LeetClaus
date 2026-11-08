from db import auth, user_data
from helperfunctions.leetcodeAPI import confirmLeetCodeUser
import bcrypt
from helperfunctions.progress import newUserDataDoc
import string
def handleLogin(request):
    formresponses = request.form.to_dict()
    userInfo = auth.find_one({"username": formresponses["username"]})
    if userInfo is None:
        return "Invalid username or password"
    passAttempt = formresponses["password"].encode()
    if not bcrypt.checkpw(passAttempt, userInfo["hashedPass"]):
        return "Invalid username or password"
    return "passed"
def createNewAccount(request):
    result = validateAccount(request)
    if result == 'passed':
        formResponses = request.form.to_dict()
        encodedpass = formResponses["password"].encode()
        prefList = makePrefList(request)
        salt = bcrypt.gensalt()
        hashedpass = bcrypt.hashpw(encodedpass, salt)
        newUser = {
            "username":formResponses["username"],
            "hashedPass": hashedpass,
            "leetcode_username":formResponses["leetcode_username"]
        }
        newUserData = newUserDataDoc(formResponses["username"], formResponses["leetcode_username"],prefList)
        auth.insert_one(newUser)
        user_data.insert_one(newUserData)
    return result
def makePrefList(request):
    # build the list ourselves from which boxes were ticked, so only these three exact values can end up in the API URL
    prefList = []
    for field, difficulty in (("easy", "EASY"), ("medium", "MEDIUM"), ("hard", "HARD")):
        if request.form.get(field) is not None:
            prefList.append(difficulty)
    if prefList == []:
        prefList = ["EASY", "MEDIUM", "HARD"]
    return prefList

def validateAccount(request):
    formResponses = request.form.to_dict()
    #leetcode user is real
    if (confirmLeetCodeUser(formResponses["leetcode_username"]) == False):
        return "Leetcode username doesn't exist"
    #username isn't taken
    elif (auth.find_one({"username": formResponses["username"]}) is not None):
        return "Username already taken"
    #leetcode isn't alr claimed
    elif (auth.find_one({"leetcode_username": formResponses["leetcode_username"]}) is not None):
        return "Leetcode user already claimed"
    #passwords match (duh)
    elif (formResponses["password"] != formResponses["confirm_password"]):
        return "Passwords dont match"
    #check password strength
    elif (len(formResponses["password"]) < 8):
        return "Password must be at least 8 character"
    elif (len(formResponses["password"]) > 40):
        return "Password must be less than 40 character"
    elif (len(formResponses["username"]) > 40):
        return "Username must be less than 40 character"
    else:
        specialChars = string.punctuation
        symbol = False
        number = False
        for char in formResponses["password"]:
            if char in specialChars:
                symbol = True
            elif char.isdigit():
                number = True
        if symbol and number:
            return "passed"
        else:
            return "Make sure your password has a special character and number"
