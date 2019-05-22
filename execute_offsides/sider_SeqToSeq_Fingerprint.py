import deepchem as dc
from deepchem.models.tensorgraph.optimizers import Adam, ExponentialDecay
import numpy as np

import datetime

import sys
print(sys.version)

print("Inicio : %s" % datetime.datetime.now())

tokens = set()

tasks, datasets, transformers = dc.molnet.load_sider()
train_dataset, valid_dataset, test_dataset = datasets
train_smiles = train_dataset.ids
valid_smiles = valid_dataset.ids


print(train_smiles.size)

tokens = set()
for s in train_smiles:
  tokens = tokens.union(set(c for c in s))
tokens = sorted(list(tokens))

print(tokens[0:5])

max_length = max(len(s) for s in train_smiles)
model = dc.models.SeqToSeq(tokens,
                           tokens,
                           max_length,
                           encoder_layers=2,
                           decoder_layers=2,
                           embedding_dimension=256,
                           model_dir='fingerprint')
batches_per_epoch = len(train_smiles)/model.batch_size

model.set_optimizer(Adam(learning_rate=ExponentialDecay(0.004, 0.9, batches_per_epoch)))

def generate_sequences(epochs):
  for i in range(epochs):
    for s in train_smiles:
      yield (s, s)

model.fit_sequences(generate_sequences(40))


predicted = model.predict_from_sequences(valid_smiles[:500])
count = 0
for s,p in zip(valid_smiles[:500], predicted):
  if ''.join(p) == s:
    count += 1
print('reproduced', count, 'of 500 validation SMILES strings')

train_embeddings = model.predict_embeddings(train_smiles)
train_embeddings_dataset = dc.data.NumpyDataset(train_embeddings,
                                                train_dataset.y,
                                                train_dataset.w,
                                                train_dataset.ids)

valid_embeddings = model.predict_embeddings(valid_smiles)
valid_embeddings_dataset = dc.data.NumpyDataset(valid_embeddings,
                                                valid_dataset.y,
                                                valid_dataset.w,
                                                valid_dataset.ids)

test_embeddings = model.predict_embeddings(test_smiles)
test_embeddings_dataset = dc.data.NumpyDataset(test_embeddings,
                                               test_dataset.y,
                                               test_dataset.w,
                                               test_dataset.ids)


classifier = dc.models.MultiTaskClassifier(n_tasks=len(tasks),
                                                      n_features=256,
                                                      layer_sizes=[512])

classifier.fit(train_embeddings_dataset, nb_epoch=10)


import numpy as np
metric = dc.metrics.Metric(dc.metrics.roc_auc_score, np.mean, mode="classification")
train_score = classifier.evaluate(train_embeddings_dataset, [metric], transformers)
valid_score = classifier.evaluate(valid_embeddings_dataset, [metric], transformers)

print('Training set ROC AUC:', train_score)
print('Validation set ROC AUC:', valid_score)

test_score = classifier.evaluate(test_embeddings_dataset, [metric], transformers)

print('Test set ROC AUC:', test_score)

print("Fim : %s" % datetime.datetime.now())
