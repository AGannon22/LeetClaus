from db import auth_db
def handleLogin(request):
    pass
def validateAccount(request):
    print(request, request.form.to_dict())
    formResponses = request.form.to_dict()
    print(formResponses)