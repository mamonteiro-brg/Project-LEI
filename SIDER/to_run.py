from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import warnings
warnings.filterwarnings('ignore')

import numpy as np
import tensorflow as tf
import deepchem as dc
from deepchem.models.tensorgraph.models.graph_models import GraphConvModel


sider_tasks, sider_datasets, transformers = dc.molnet.load_sider(featurizer='GraphConv')
train_dataset, valid_dataset, test_dataset = sider_datasets


num_epochs = 10
losses = []

model = GraphConvModel(
    len(sider_tasks), batch_size=50, mode='classification')

for i in range(num_epochs):
    # Set nb_epoch=10 for better results.
    loss = model.fit(train_dataset, nb_epoch=1)
    print("Epoch %d loss: %f" % (i, loss))
    losses.append(loss)
    
metric = dc.metrics.Metric(
    dc.metrics.roc_auc_score, np.mean, mode="classification")

print("Evaluating model")
train_scores = model.evaluate(train_dataset, [metric], transformers)
print("Training ROC-AUC Score: %f" % train_scores["mean-roc_auc_score"])

valid_scores = model.evaluate(valid_dataset, [metric], transformers)
print("Validation ROC-AUC Score: %f" % valid_scores["mean-roc_auc_score"])


num_epochs = 50
losses = []

model = GraphConvModel(
    len(sider_tasks), batch_size=50, mode='classification')
# Set nb_epoch=10 for better results.

for i in range(num_epochs):
    # Set nb_epoch=10 for better results.
    loss = model.fit(train_dataset, nb_epoch=1)
    print("Epoch %d loss: %f" % (i, loss))
    losses.append(loss)
    
    
metric = dc.metrics.Metric(
    dc.metrics.roc_auc_score, np.mean, mode="classification")

print("Evaluating model")
train_scores = model.evaluate(train_dataset, [metric], transformers)
print("Training ROC-AUC Score: %f" % train_scores["mean-roc_auc_score"])


valid_scores = model.evaluate(valid_dataset, [metric], transformers)
print("Validation ROC-AUC Score: %f" % valid_scores["mean-roc_auc_score"])


params_dict = {'batch_size' : [32,64,128,256],
               'nb_epoch': [10,100,200],
               'learning_rate': [0.0005,0.5,0.75,1],
               'n_filters': [32,64,128,256],
               'n_fully_connected_nodes' : [32,64,128,256]
              }
              
n_features = len(train_dataset)

def model_builder(model_params, model_dir):
    model = GraphConvModel(
            len(sider_tasks), mode='classification',**model_params)
    
    return model


metric = dc.metrics.Metric(dc.metrics.roc_auc_score, np.mean)
optimizer = dc.hyper.HyperparamOpt(model_builder)
best_dnn, best_hyperparams, all_results = optimizer.hyperparam_search(
   params_dict, train_dataset, valid_dataset, [], metric)
   
   
   