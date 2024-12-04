class LoginError(Exception):
    def __str__(self):
        return "login failed"


class RoleError(Exception):
    def __str__(self):
        return "role error"


class NotFoundError(Exception):
    def __str__(self):
        return "not found error"


class TokenError(Exception):
    def __str__(self):
        return "token error"


class TokenKeyError(Exception):
    def __str__(self):
        return "there is no jwt key"
