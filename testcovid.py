#%%
from quipus import HLNB_BC, Quipus, Quipus2, Quipus3
import tools
import numpy as np
from sklearn.model_selection import cross_val_predict
from sklearn.model_selection import train_test_split, cross_val_score, cross_val_predict
from sklearn.model_selection import KFold, ShuffleSplit, StratifiedKFold, GridSearchCV
import time
from sklearn.metrics import confusion_matrix


strNameDataset = "glcmCovid19"
dataset = tools.getDataFromCSV("./dataset/" + strNameDataset + ".csv")
print("DATASET: " + strNameDataset)
print("---------")
seed = int(time.time())
# # kfold = KFold(n_splits=10, random_state=seed, shuffle=True)
# kfold = StratifiedKFold(n_splits=10, shuffle=True, random_state=seed)
# print("Partitions: " + str(seed))

# # grid_param = {
# #     "knn": range(1, 10),
# #     "ePercentile": [0.0, 0.5, 1.0],
# #     "bnn": [1, 3, 5],
# #     "alpha": [0.0, 0.5, 1.0],
# # }
# grid_param = {
#     "knn": range(7, 11),
#     "ePercentile": [0.0, 0.5],
#     "bnn": [1, 3],
#     "alpha": [0.0, 0.5, 1.0],
# }

# quipusClass = Quipus3()

# gd_sr = GridSearchCV(
#     estimator=quipusClass,
#     param_grid=grid_param,
#     scoring="accuracy",
#     cv=kfold.split(dataset["data"], dataset["target"]),
# )
# gd_sr.fit(dataset["data"], dataset["target"])

# best_parameters = gd_sr.best_params_
# print(best_parameters)
# print(gd_sr.best_score_)
# print("---------")
#%%
test = 1
total = []
# knnTest = best_parameters["knn"]
# ePercentile = best_parameters["ePercentile"]
# bnnTest = best_parameters["bnn"]
# alpha = best_parameters["alpha"]

knnTest = 5
ePercentile = 0.0
bnnTest = 3
alpha = 0.0

print("knn: ", knnTest)
print("e-percentile: ", ePercentile)
print("bnn: ", bnnTest)
print("alpha: ", alpha)

for i in range(test):
    quipusClass = Quipus3(
        knn=knnTest, ePercentile=ePercentile, bnn=bnnTest, alpha=alpha
    )
    kfold = StratifiedKFold(n_splits=10, random_state=i + seed, shuffle=True)
    scores = cross_val_score(
        quipusClass,
        dataset["data"],
        dataset["target"],
        scoring="accuracy",
        cv=kfold.split(dataset["data"], dataset["target"]),
    )
    total.append(scores)
total = np.array(total)
np.savetxt(
    "./Tests/"
    + str(seed)
    + " "
    + strNameDataset
    + " scores "
    + str(total.mean())
    + "pm"
    + str(total.std() * 2)
    + " "
    + str(quipusClass)
    + "knn "
    + str(knnTest)
    + " e "
    + str(ePercentile)
    + " bnn "
    + str(bnnTest)
    + " alpha "
    + str(alpha),
    total,
    delimiter=",",
)
print("--------")
print(total.mean(), total.std())
print("---------")
#%%
quipusClass = Quipus3(
        knn=knnTest, ePercentile=ePercentile, bnn=bnnTest, alpha=alpha
    )
y_pred = cross_val_predict(quipusClass, dataset["data"],dataset["target"], cv=10)
conf_mat = confusion_matrix(dataset["target"], y_pred)

np.savetxt(
    "./Tests/cm/"
    + str(seed)
    + " "
    + strNameDataset
    + " scores "
    + str(total.mean())
    + "pm"
    + str(total.std() * 2)
    + " "
    + str(quipusClass)
    + "knn "
    + str(knnTest)
    + " e "
    + str(ePercentile)
    + " bnn "
    + str(bnnTest)
    + " alpha "
    + str(alpha),
    conf_mat,
    delimiter=",",
)
#%%
import matplotlib.pyplot as plt
data=np.genfromtxt('./Tests/covidResults.csv', delimiter=',')
plt.figure()
plt.boxplot(data.flatten())
#%%

# import numpy as np
# import random
# import math
# from matplotlib import pyplot as plt

# data = np.genfromtxt("./Tests/eval.csv", delimiter=",")
# data = data.flatten()
# # # fixed bin size
# # # bins = np.arange(-100, 100, 5) # fixed bin size
# # bins = np.linspace(math.ceil(min(data)),
# #                    math.floor(max(data)),
# #                    5) # fixed number of bins


# # plt.xlim([min(data), max(data)])

# plt.hist(data, 20)
# # plt.title('Random Gaussian data (fixed bin size)')
# # plt.xlabel('variable X (bin size = 5)')
# # plt.ylabel('count')

# plt.show()

# %%
