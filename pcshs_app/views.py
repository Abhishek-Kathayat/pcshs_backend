from django.shortcuts import render
from django.http import HttpResponse
import json

# Create your views here.
def processHeartData(request):
    hrtdata = request.body.decode('utf-8')
    heart_data = json.load(hrtdata)
    for key, value in heart_data.items():
        print(key, ':', value)
