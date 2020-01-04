from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
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

def datacompute(hrt_data):
    import statistics
    import pandas as pd
    import numpy as np
    from sklearn.preprocessing import StandardScaler
    from sklearn.model_selection import train_test_split

    import torch
    import torch.nn as nn
    import torch.nn.functional as F
    from torch.autograd import Variable
    torch.manual_seed(42)

    FILE_PATH = 'C:/Users/abhis/Documents/PCSHS_Backend/pcshs_backend/pcshs_app/data/heart_data.csv'
    data = pd.read_csv(FILE_PATH)

    X = data.iloc[:, 0:13].values
    y = data.iloc[:, 13].values
    X_standard = StandardScaler().fit_transform(X)
    dataNormalize = pd.DataFrame(X_standard, index = data.index,
                                columns = data.columns[0:13])
    dataNormalize['target'] = data['target']

    X = dataNormalize.iloc[:, 0:13].values
    y = dataNormalize.iloc[:, 13].values

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3,
                                                       random_state = 0)
    new_data = list()
    for i in range(0, len(data.columns) - 1):
        x_data = data.iloc[0:, i].values
        x_data = x_data.tolist()
        x_data.append(hrt_data[i])
        new_data.append((hrt_data[i] - statistics.mean(x_data)) / statistics.stdev(x_data))

    new_data = np.asarray(new_data)
    new_data = np.reshape(new_data, [1, 13])

    xtrain = X_train
    ytrain = y_train

    h1 = 6
    h2 = 4
    lr = 0.0023
    num_epochs = 7000

    class Net(nn.Module):
        def __init__(self):
            super(Net, self).__init__()
            self.fc1 = nn.Linear(13, h1)
            self.fc2 = nn.Linear(h1, h2)
            self.fc3 = nn.Linear(h2, 2)
        def forward(self, x):
            x = F.relu(self.fc1(x))
            x = F.relu(self.fc2(x))
            x = self.fc3(x)
            return x

    net = Net()
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.SGD(net.parameters(), lr = lr, momentum = 0.7)
    loss_per_epochs = []

    for epoch in range(num_epochs):
        X = Variable(torch.Tensor(xtrain).float())
        Y = Variable(torch.Tensor(ytrain).long())
        optimizer.zero_grad()
        out = net(X)
        loss = criterion(out, Y)
        loss.backward()
        optimizer.step()

        loss_per_epochs.append(loss.item())

    epochs = np.arange(1, num_epochs + 1)
    X = Variable(torch.Tensor(new_data).float())
    out = net(X)
    _, predicted = torch.max(out.data, 1)
    return predicted.item()


@csrf_exempt
def processHeartData(request):
    hrtdata = request.body.decode('utf-8')
    heart_data = json.loads(hrtdata)

    # Process Data.
    hrt_data = dataprocess(heart_data)
    result_hrtdata = datacompute(hrt_data)
    
    result = ''
    if result_hrtdata == 1:
        result = 'Heart Disease Detected'
    else:
        result = 'No Heart Disease Detected'

    return JsonResponse({
        'result': result
    })
