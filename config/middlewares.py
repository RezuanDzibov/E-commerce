from rest_framework import response
from django.http.response import JsonResponse


class Except:
    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        return self._get_response(request)

    def process_exception(self, request, exception):
        return JsonResponse(data={"detail": str(exception)})
        