from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.
@csrf_exempt
def processHeartData(request):
    hrtdata = request.body.decode('utf-8')
    heart_data = json.loads(hrtdata)

    # Process Data.
    hrt_data = list()
    for key, value in heart_data['body'].items():
        if(key == 'Gender_js'):
            if value == 'Male':
                hrt_data.append(1)
            else:
                hrt_data.append(0)
        elif(key == 'chptype_js'):
            if value == 'Typical Angina':
                hrt_data.append(1)
            elif value == 'Atypical Angina':
                hrt_data.append(2)
            elif value == 'Non-Anginal Pain':
                hrt_data.append(3)
            else:
                hrt_data.append(4)
        elif(key == 'bsl_js'):
            if value == 'True':
                hrt_data.append(1)
            else:
                hrt_data.append(0)
        elif(key == 'rer_js'):
            if value == 'Normal':
                hrt_data.append(0)
            elif value == 'Having ST-T wave abnormality':
                hrt_data.append(1)
            else:
                hrt_data.append(2)
        elif(key == 'eia_js'):
            if value == 'Yes':
                hrt_data.append(1)
            else:
                hrt_data.append(0)
        elif(key == 'slpst_js'):
            if value == 'Upsloping':
                hrt_data.append(0)
            elif value == 'Flat':
                hrt_data.append(1)
            else:
                hrt_data.append(2)
        elif(key == 'thal_js'):
            if value == 'Normal':
                hrt_data.append(1)
            elif value == 'Fixed Defect':
                hrt_data.append(2)
            else:
                hrt_data.append(3)
        elif(key == 'stdep_js'):
            hrt_data.append(float(value))
        else:
            hrt_data.append(int(value))

    print(hrt_data)
    return HttpResponse('OK')
