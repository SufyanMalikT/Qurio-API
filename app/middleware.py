import time 

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]  # In case of multiple IPs
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
class TimerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start = time.time()
        response = self.get_response(request)
        print(get_client_ip(request))
        duration = time.time() - start
        print(f"Request took {duration:.2f} seconds.")
        return response