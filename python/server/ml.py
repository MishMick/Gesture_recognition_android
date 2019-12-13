import pandas as pd
import numpy as np
import warnings
from sklearn.linear_model import Perceptron, LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.decomposition import PCA
from sklearn.neural_network import MLPClassifier
#import matplotlib.pyplot as plt
import glob
import os
import vidproc
from sklearn.preprocessing import StandardScaler




def make_models(data, target):

    #data = dopca(data, 14)

    print("models to me")

    perc = Perceptron(random_state=0, max_iter=1000, tol=-np.inf, penalty='l1')
    perc.fit(data, target)

    logre = LogisticRegression(random_state=0, multi_class='auto', C=1, max_iter=10000, solver='lbfgs', tol=.0001)
    logre.fit(data, target)

    #svma = SVC(random_state=0, gamma='scale', max_iter=1000, C=10)
    #svma.fit(data, target)
#
    #tree = DecisionTreeClassifier(random_state=0, criterion='entropy', max_depth=6)
    #tree.fit(data, target)
#
    knei = KNeighborsClassifier(algorithm='auto', n_neighbors=1)
    knei.fit(data, target)

    mlpc = MLPClassifier(hidden_layer_sizes=(100, 10), activation='relu', learning_rate='constant', solver='sgd', max_iter=10000)
    mlpc.fit(data, target)

    print("models go")

    return [perc, logre, knei,  mlpc] #tree, svma,

def query_models(models, scaler, folder):
    vidproc.convert_to_csv(folder + "/")
    query = extract_features(folder + "/keypoints.csv").reshape(1, -1)
    query = scaler.transform(query)
    #data = np.vstack([data, query])
    #data = dopca(data, 14)
    #query = data.tail(1)
    ans = [ model.predict(query)[0] for model in models ]
    #print(json(ans))     
    return json(ans)


def json(ans):
    #res = "{ “1”: “predicted_label”, “2”: “predicted_label”, “3”: “predicted_label”, “4”: “predicted_label” }"
    res = "{ "
    for i in range(len(ans)):
        res = res + '"' + str(i + 1) + '": "' + ans[i] + '"'
        if(i != len(ans) - 1):
            res = res + ', '

    res = res + ' }'
    return res


## use PCA on a dataset
def dopca(data, size):
    pca = PCA(n_components=size)
    temp = pca.fit_transform(data)
    redata = pd.DataFrame(data=temp)
    return redata


## sweep pca size over all learning algorythm params
def pcasweep(sizes, data, target):
    for i in sizes:
        print()
        print("PCA SIZE", i)
        redata = dopca(data, i)
        analyze(redata, target)
    return


def analyze(dataset, target):

    # Perceptron Params
    perc = Perceptron(random_state=0)
    params = dict(max_iter=[1000, 10000], tol=[-np.inf, .0001, .001, .01], penalty=[None, 'l1', 'l2', 'elasticnet'])
    #params = dict(max_iter=[10000], tol=[-np.inf, .001, .1], penalty=[None, 'l1', 'l2', 'elasticnet'])
    print("Perceptron sweep")
    #grid(perc, params, dataset, target)

    # Logistic Regression Params
    logre = LogisticRegression(random_state=0, multi_class='auto')
    params = dict(max_iter=[10000], solver=['lbfgs', 'liblinear', 'sag', 'saga', 'newton-cg'], C=range(1, 20, 3), tol=[.0001, .001])
    #params = dict(max_iter=[100, 1000], solver=['saga'], C=range(1, 20, 3), tol=[.001, .1])
    print("LogReg sweep")
    #grid(logre, params, dataset, target)

    # SVC Params
    svma = SVC(random_state=0, gamma='scale')
    params = dict(max_iter=[1000], C=range(1, 20, 1))
    print("SVC sweep")
    #grid(svma, params, dataset, target)

    # Tree Params TODO MORE PARAMS
    tree = DecisionTreeClassifier(random_state=0)
    params = dict(max_depth=range(1, 20, 1), criterion=['gini', 'entropy'])
    print("decision tree sweep")
    #grid(tree, params, dataset, target)

    # KNeighbors Params
    knei = KNeighborsClassifier(algorithm='auto')
    params = dict(n_neighbors=range(1, 20, 1))
    print("kneighbors sweep")
    #grid(knei, params, dataset, target)

    # NN Params
    mlpc = MLPClassifier(hidden_layer_sizes=(100, 10))
    params = dict(activation=['identity', 'logistic', 'tanh', 'relu'], solver=['lbfgs', 'sgd', 'adam'], learning_rate=['constant', 'invscaling', 'adaptive'], max_iter=[10000])
    print("NN sweep")
    grid(mlpc, params, dataset, target)

    return


## sweep function
def grid(estimator, params, dataset, target):
    clf = GridSearchCV(estimator=estimator, param_grid=params)
    clf.fit(dataset, target)
    print(clf.best_score_, clf.best_params_)
    return


def main():
    ## ignore warnings
    #warnings.filterwarnings("ignore")
    
    data, target = gather()
    
    #data, target = load_data()

    #models = make_models(data, target)

    scaler = StandardScaler()
    scaler.fit(data)
    data = scaler.transform(data)

    analyze(data, target)
    #pcasweep(range(25, 40, 10), data, target)
    
    return

def load_data():
    data = np.load("data.npy")
    target = np.load("target.npy")
    return data, target

def save_data(data, target):
    np.save("data", data)
    np.save("target", target)
    print("data saved")
    return


def gather():
    signs = glob.glob("CSV_Thursday/CSV/*")
    data = np.vstack([ extract_sign(sign) for sign in signs ])
    target = np.vstack([ make_target(sign) for sign in signs ]).ravel()
    save_data(data, target)
    return data, target

def make_target(sign):
    _, tail = os.path.split(sign)
    samples = glob.glob(sign + "/*.csv")
    h = len(samples)
    return np.full((h, 1), tail)


def extract_sign(sign):
    samples = glob.glob(sign + "/*.csv")
    return np.vstack([ extract_features(sample) for sample in samples ])


def extract_features(sample):
    #print(sample)
    data = pd.read_csv(sample, header=0, index_col=0)

    #if(len(data.index) > 165):
    #    print(sample)

    #print(data.head())
    ymin = (data['leftHip_y'].median() + data['rightHip_y'].median())/2
    ymax = (data['leftShoulder_y'].median() + data['rightShoulder_y'].median())/2
    #print(ymax - ymin, sample)
    xmax = data['leftShoulder_x'].median()
    xmin = data['rightShoulder_x'].median()
    #print(xmin, xmax)

    ## norm
    #print(data[['leftWrist_x', 'rightWrist_x', ]])
    data[['leftWrist_x', 'rightWrist_x', 'leftElbow_x', 'rightElbow_x',]] = (data[['leftWrist_x', 'rightWrist_x', 'leftElbow_x', 'rightElbow_x',]] - xmin) / (xmax - xmin)
    data[['leftWrist_y', 'rightWrist_y', 'leftElbow_y', 'rightElbow_y',]] = (data[['leftWrist_y', 'rightWrist_y', 'leftElbow_y', 'rightElbow_y',]] - ymin) / (ymax - ymin)

    #data[['leftWrist_x', 'leftWrist_y', 'rightWrist_x', 'rightWrist_y',]] = data[['leftWrist_x', 'leftWrist_y', 'rightWrist_x', 'rightWrist_y',]] * 2
    
    #data['y'] = data['leftWrist_y'] - data['rightWrist_y']
    #data['x'] = data['leftWrist_x'] - data['rightWrist_x']
    #print(data[['leftWrist_x', 'rightWrist_x', ]])

    ## extend to LEN features by replicating last frame
    LEN = 150
    if(len(data.index) > LEN):
        data = data.head(LEN)
    else:
        #median = data.iloc[int(len(data.index)/2)]
        #median = median * 0
        #mean = data.mean(axis=0)
        #print(mean)
        while(len(data.index) < LEN):
        #    data = data.append(median)
            data = data.append(data.tail(1))
        #    data = data.append(mean, ignore_index=True)
        #while(len(data.index) < LEN):
        #    data = data.append(data.head(LEN - len(data.index)))
        
    
    features = data[['leftWrist_x', 'leftWrist_y', 'rightWrist_x', 'rightWrist_y', 'leftElbow_x', 'leftElbow_y', 'rightElbow_x', 'rightElbow_y']].to_numpy().T.flatten()
    
    #print(features)

    #features = pd.DataFrame()
    #features["lw"] = (((data["leftWrist_x"] - data["nose_x"]) * (data["leftWrist_y"] - data["nose_y"]))) / (data["leftEye_x"] - data["rightEye_x"])
    #features["rw"] = (((data["rightWrist_x"] - data["nose_x"]) * (data["rightWrist_y"] - data["nose_y"]))) / (data["leftEye_x"] - data["rightEye_x"])
    #features["le"] = (((data["leftWrist_x"] - data["nose_x"]) * (data["leftWrist_y"] - data["nose_y"]))) / (data["leftEye_x"] - data["rightEye_x"])
    #features["re"] = (((data["rightWrist_x"] - data["nose_x"]) * (data["rightWrist_y"] - data["nose_y"]))) / (data["leftEye_x"] - data["rightEye_x"])
    #ret = features.to_numpy().T.flatten()
        
    return features


if __name__ == '__main__':
    main()