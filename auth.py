from flask import request
from functools import wraps
import requests

AUTH_SERVER = "https://auth.hack.courses/"

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        user = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
        if not token:
            return {
                "message": "Authentication Token is missing!",
                "data": None,
                "error": "Unauthorized"
            }, 401
        try:
            r = requests.post(AUTH_SERVER+"check_token", data={"token": token})
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
        token = None
        user = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
        try:
            r = requests.post(AUTH_SERVER+"check_token", data={"token": token})
            if r.status_code == 200:
                user = r.json()
        except Exception as e:
            return {
                "message": "Something went wrong",
                "data": None,
                "error": str(e)
            }, 500

        return f(user, *args, **kwargs)
    return decorated