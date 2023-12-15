from flask import request
from functools import wraps
import requests

AUTH_SERVER = "http://127.0.0.1:5001/"

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user = None
        print(request)
        token = request.cookies.get("h_courses_auth")
        if not token and "Authorization" not in request.headers:
            return {
                "message": "Authentication Token is missing!",
                "data": None,
                "error": "Unauthorized"
            }, 401
        try:
            r = requests.post(AUTH_SERVER+"check_token", headers={"Authorization": request.headers.get("Authorization")}, cookies=request.cookies)
            if r.status_code != 200:
                return {
                "message": "Invalid Authentication token!",
                "data": None,
                "error": "Unauthorized"
            }, 401
            user = r.json()
        except Exception as e:
            return {
                "message": "Something went wrong",
                "data": None,
                "error": str(e)
            }, 500

        return f(user, *args, **kwargs)
    return decorated

def token_optional(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get("h_courses_auth")
        user = None
        try:
            r = requests.post(AUTH_SERVER+"check_token", headers={"Authorization": request.headers.get("Authorization")}, cookies=request.cookies)
            if r.status_code == 200:
                user = r.json()
        except Exception as e:
            print(e)
#            return {
#                "message": "Something went wrong",
#                "data": None,
#                "error": str(e)
#            }, 500

        return f(user, *args, **kwargs)
    return decorated