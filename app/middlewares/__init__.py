from .auth import AuthMiddleware

middlewares: list[AuthMiddleware] = [
    AuthMiddleware
]