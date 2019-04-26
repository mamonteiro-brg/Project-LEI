import deepchem as dc
from deepchem.models.tensorgraph.optimizers import Adam, ExponentialDecay

tokens = set()

def generate_sequences(epochs):
    for i in range(epochs):
        for s in train_smiles:
            yield (s, s)

            
def loadData():
    tasks, datasets, transformers = dc.molnet.load_sider()
    train_dataset, valid_dataset, test_dataset = datasets
    train_smiles = train_dataset.ids
    valid_smiles = valid_dataset.ids

    print ("a small expample") 

    max_length = max(len(s) for s in train_smiles)
    model = dc.models.SeqToSeq(tokens,tokens,max_length,encoder_layers=2,decoder_layers=2,embedding_dimension=256,model_dir='fingerprint')
    batches_per_epoch = len(train_smiles)/model.batch_size
    model.set_optimizer(Adam(learning_rate=ExponentialDecay(0.004, 0.9, batches_per_epoch)))
    
    print ("a small expample")
    
    model.fit_sequences(generate_sequences(40))
        

def defineTokens():
    for s in train_smiles:
        tokens = tokens.union(set(c for c in s))
    tokens = sorted(list(tokens))

    
def main(): 
    # function calling 
    #loadData()              
    generate_sequences(40)
    
# Main function calling 
if __name__=="__main__":       
    main() 