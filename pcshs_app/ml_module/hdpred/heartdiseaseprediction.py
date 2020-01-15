def hdprediction(hrt_data):
    # Heart Disease Prediction Model.
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
