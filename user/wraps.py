from functools import wraps
from django.http import JsonResponse , HttpRequest
from .auth import decode_jwt



def jwt_must(func):
    @wraps(func)
    def wrapper(request : HttpRequest, *args, **kwargs):
        
        auth: str | None = request.headers.get("Auth")
        
        if not auth or not auth.startswith("Bearer "):
            return JsonResponse({"error": "Unauthorized"}, status=401)
        
        token = auth.split(" ")[1]
        
        data = decode_jwt(token)
        
        if not data or data == "expired" or data.get("type") != 'access': # type: ignore
            return JsonResponse({"error": "invalid token"}, status=401)
        
        request.user_id = data["user_id"] # type: ignore
        request.role = data["role"] # type: ignore
        
        return func(request , *args, **kwargs)
        
    return wrapper


def role_required(roles):
    def dec(func):
        @wraps(func)
        def wrapper(request : HttpRequest, *args, **kwargs):
            if request.role not in roles: # type: ignore
                return JsonResponse({"error": "you do not have permission"}, status=403)
            return func(request , *args, **kwargs)
        return wrapper
    return dec
        


