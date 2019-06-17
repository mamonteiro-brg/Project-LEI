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


