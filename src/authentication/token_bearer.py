from rest_framework.authentication import TokenAuthentication


class TokenBearerAuthentication(TokenAuthentication):
    keyword = "Bearer"
