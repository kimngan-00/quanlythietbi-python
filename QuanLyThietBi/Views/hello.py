from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def hello_world(request):
    """
    API endpoint trả về Hello World
    """
    if request.method == 'GET':
        return JsonResponse({
            'message': 'Hello World!',
            'status': 'success'
        })
    else:
        return JsonResponse({
            'error': 'Method not allowed',
            'status': 'error'
        }, status=405)
