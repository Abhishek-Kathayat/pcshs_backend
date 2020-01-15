from django.shortcuts import render
from .models import ECGFiles
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pcshs_app.ml_module.hdpred.heartdiseaseprediction import hdprediction
import json

# Create your views here.
def dataprocess(heart_data):
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

    return hrt_data;

@csrf_exempt
def processHeartData(request):
    hrtdata = request.body.decode('utf-8')
    heart_data = json.loads(hrtdata)

    # Process Data.
    hrt_data = dataprocess(heart_data)
    result_hrtdata = hdprediction(hrt_data)

    result = ''
    if result_hrtdata == 1:
        result = 'Heart Disease Detected'
    else:
        result = 'No Heart Disease Detected'

    return JsonResponse({
        'result': result
    })

def signalExtract():
    import wfdb
    import os

    ECG_FILES = 'C:/Users/abhis/Documents/PCSHS_Backend/pcshs_backend/ecg_files'
    files = os.listdir(ECG_FILES)
    fname = files[0].split('.')[0]
    record = wfdb.rdrecord(ECG_FILES + '/100')
    return record.p_signal

@csrf_exempt
def processECGData(request):
    file_store = request.FILES.items()
    for key, value in file_store:
        obj = ECGFiles.objects.create(file = value)

    p_signal = signalExtract()
    p_signal = p_signal.tolist()

    ml2 = list()
    v5 = list()
    for values in p_signal:
        ml2.append(values[0])
        v5.append(values[1])

    return JsonResponse({
        'ml2signal': ml2,
        'v5signal': v5
    })
