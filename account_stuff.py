from db import auth, user_data
from helperfunctions.leetcodeAPI import confirmLeetCodeUser
def handleLogin(request):
    pass
def createNewAccount(request):
    # returns "passed" on success, otherwise the error message to show the user
    result = validateAccount(request)
    if result == 'passed':
        pass  # TODO: insert the new account into auth / user_data
    return result

def validateAccount(request):
    print(request, request.form.to_dict())
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
    #check password strength, TODO I want to check symbols and numbers included later
    elif (len(formResponses["password"]) < 8):
        return "Use a stronger password"
    else:
        return "passed"