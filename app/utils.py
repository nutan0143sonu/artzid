'''Student Module'''
from rest_framework.views import exception_handler
from django.http import Http404


def custom_exception_handler(exc, context):
    '''docstring'''
    response = exception_handler(exc, context)
    if isinstance(exc, Http404):
        response.data = {
            'data': 'Data does not exist'
        }
        return response
    try:
        if 'email' in exc.get_codes() and 'unique' in exc.get_codes()['email']:
            response.data = {
                'message': 'This Email already exist.'
            }
            return response
    except:
        return response

