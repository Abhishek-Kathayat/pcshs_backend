import sys
import json
import keras
import numpy as np
import scipy.io as sio
import scipy.stats as sst

sys.path.insert(0, 'C:/Users/abhis/Documents/BTCSE Project/pcshs_backend/support_files')
import load
import network
import util

def predict(record):
    FILE_PATH = "C:/Users/abhis/Documents/BTCSE Project/pcshs_backend/support_files/"
    ecg = load.load_ecg(record +".mat")
    preproc = util.load(".")
    x = preproc.process_x([ecg])

    params = json.load(open(FILE_PATH + "config.json"))
    params.update({
        "compile" : False,
        "input_shape": [None, 1],
        "num_categories": len(preproc.classes)
    })

    model = network.build_network(**params)
    model.load_weights(FILE_PATH + 'model/model.hdf5')

    probs = model.predict(x)
    prediction = sst.mode(np.argmax(probs, axis=2).squeeze())[0][0]
    return preproc.int_to_class[prediction]
