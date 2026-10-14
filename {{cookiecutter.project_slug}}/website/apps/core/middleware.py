from secure import Secure


class SecureHeadersMiddleware:
    """
    Process requests and return a secure response using "secure" library
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.secure = Secure.with_default_headers()

    def __call__(self, request):
        response = self.get_response(request)
        self.secure.set_headers(response)
        return response
