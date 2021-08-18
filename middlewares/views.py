from django.shortcuts import render
from django.core.exceptions import PermissionDenied  
from django.http import JsonResponse
import json



class SetResponseHeaderMiddleware:
    def __init__(self, next_request_handler):
        self.next_request_handler = next_request_handler
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before

        response = self.next_request_handler(request)

        content_type = response.headers.get('Content-Type','')

        if content_type == 'application/json' :
            response = json.loads(response.content.decode('utf8'))
            response['token'] = 'This is a test token'
            return JsonResponse(response)
        else:
            return response



def ip_filter_middleware(request_handler_function):
    # One-time configuration and initialization.

    def middleware(request):
        # Code to be executed for each request before
        
        filter_ips = ['192.168.1.1', '123.123.123.123']
        ip = request.META.get('REMOTE_ADDR')
        if ip in filter_ips:
            data = {'error':'Access from this IP address is Not allowed'}
            return JsonResponse(data,status=400)
        
        
        response = request_handler_function(request)
        # Code to be executed for each request before
        
        return response

    return middleware