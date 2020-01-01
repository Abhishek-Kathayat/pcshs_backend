from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.
@csrf_exempt
def processHeartData(request):
    hrtdata = request.body.decode('utf-8')
    heart_data = json.loads(hrtdata)
    for key, value in heart_data.items():
        print(key, ':', value)
    return HttpResponse('OK')
