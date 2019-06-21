#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 17:11:47 2019

@author: angelabarros
"""

import urllib.request, urllib.error, urllib.parse
import json
import os
import pandas as pd
import csv

REST_URL = "http://data.bioontology.org"
API_KEY = "apikey token=f05c3f4e-584c-4e76-a4a9-0ee3e8fccc5c"


data = pd.read_csv("offsides_socs_1_1.csv", sep=',' ,error_bad_lines=False, index_col=False) 
data

cuis = data["umls_id"]
drugs = data["drug"]
combined = data.loc[:,['umls_id','drug']]

df = pd.DataFrame(columns={'CUI','ROOT'})

df = pd.read_excel('output2.xlsx')

list_meddras = ['Hepatobiliary disorders','Metabolism and nutrition disorders',
                                 'Product issues','Eye disorders','Investigations',
                                 'Musculoskeletal and connective tissue disorders',
                                 'Gastrointestinal disorders', 'Social circumstances',
                                 'Immune system disorders', 'Reproductive system and breast disorders',
                                 'Neoplasms benign, malignant and unspecified (incl cysts and polyps)',
                                 'General disorders and administration site conditions',
                                 'Endocrine disorders','Surgical and medical procedures',
                                 'Vascular disorders','Blood and lymphatic system disorders',
                                 'Skin and subcutaneous tissue disorders','Congenital, familial and genetic disorders',
                                 'Infections and infestations', 'Respiratory, thoracic and mediastinal disorders',
                                 'Psychiatric disorders', 'Renal and urinary disorders',
                                 'Pregnancy, puerperium and perinatal conditions', 'Ear and labyrinth disorders',
                                 'Cardiac disorders', 'Nervous system disorders',
                                 'Injury, poisoning and procedural complications']


df_final = pd.DataFrame(columns={'smiles','Hepatobiliary disorders','Metabolism and nutrition disorders',
                                 'Product issues','Eye disorders','Investigations',
                                 'Musculoskeletal and connective tissue disorders',
                                 'Gastrointestinal disorders', 'Social circumstances',
                                 'Immune system disorders', 'Reproductive system and breast disorders',
                                 'Neoplasms benign, malignant and unspecified (incl cysts and polyps)',
                                 'General disorders and administration site conditions',
                                 'Endocrine disorders','Surgical and medical procedures',
                                 'Vascular disorders','Blood and lymphatic system disorders',
                                 'Skin and subcutaneous tissue disorders','Congenital, familial and genetic disorders',
                                 'Infections and infestations', 'Respiratory, thoracic and mediastinal disorders',
                                 'Psychiatric disorders', 'Renal and urinary disorders',
                                 'Pregnancy, puerperium and perinatal conditions', 'Ear and labyrinth disorders',
                                 'Cardiac disorders', 'Nervous system disorders',
                                 'Injury, poisoning and procedural complications'})

df_aux = pd.DataFrame(columns={'CUI','smiles','SOC', 'drug'})
def get_json(url):
    opener = urllib.request.build_opener()
    opener.addheaders = [('Authorization', API_KEY)]
    return json.loads(opener.open(url).read().decode('utf-8'))

cuis = cuis.drop_duplicates()
drugs = drugs.drop_duplicates()
combined = combined.drop_duplicates("umls_id")

for item in cuis:
    try:
        search_results = get_json(REST_URL + "/search?cui="+item)
        try:
            collection = search_results.get("collection")
            if len(collection) > 0 :
                x = collection[0]
                y = x.get("links")
                url_tree = y.get("tree")
                parent_search_results = get_json(url_tree)[0]
                root_category = parent_search_results.get("prefLabel")
                df2 = pd.DataFrame([[item, root_category]], columns={'CUI','ROOT'})
                df = df.append(df2,ignore_index=True)
        except:
            print("collections deu erro no CUI "+ item)
            
        
    except:
        print("get_json do CUI "+item+ " deu erro")


df = data.loc[:,['CUI','SOC']]


for index,row in df.iterrows():
   #print(row['CUI'])
   for index2, row2 in combined.iterrows():
       if(row['CUI'] == row2['umls_id']):
           df_aux2 = pd.DataFrame([[row['CUI'],0,row['SOC'], row2['drug']]], columns={'CUI','smiles','SOC', 'drug'})
           df_aux = df_aux.append(df_aux2,ignore_index=True)
    
df.to_excel('output2.xlsx', header=True, index=False)

import pubchempy as pcp
    
import pubchempy as pcp
from pubchempy import get_compounds


for index, row in df_aux.iterrows():
    for compound in get_compounds(row['SOC'], 'name'):
        #print(compound.cid)
        #print(compound.isomeric_smiles)
        df_aux3 = pd.DataFrame([[row['CUI'],compound.isomeric_smiles, row['SOC'], row['drug']]], columns={'CUI','smiles','SOC', 'drug'})
        df_aux2 = df_aux2.append(df_aux3,ignore_index=True)
        

for index, row in df_aux2.iterrows():
    category_meddra = row['SOC']
    smile = row['smiles']
    df_final2 = pd.DataFrame([[0,0,0,smile,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]],
                             columns={'smiles','Hepatobiliary disorders','Metabolism and nutrition disorders',
                                 'Product issues','Eye disorders','Investigations',
                                 'Musculoskeletal and connective tissue disorders',
                                 'Gastrointestinal disorders', 'Social circumstances',
                                 'Immune system disorders', 'Reproductive system and breast disorders',
                                 'Neoplasms benign, malignant and unspecified (incl cysts and polyps)',
                                 'General disorders and administration site conditions',
                                 'Endocrine disorders','Surgical and medical procedures',
                                 'Vascular disorders','Blood and lymphatic system disorders',
                                 'Skin and subcutaneous tissue disorders','Congenital, familial and genetic disorders',
                                 'Infections and infestations', 'Respiratory, thoracic and mediastinal disorders',
                                 'Psychiatric disorders', 'Renal and urinary disorders',
                                 'Pregnancy, puerperium and perinatal conditions', 'Ear and labyrinth disorders',
                                 'Cardiac disorders', 'Nervous system disorders',
                                 'Injury, poisoning and procedural complications'})
    df_final = df_final.append(df_final2,ignore_index=True)



for index, row in df_final.iterrows():
    for index2, row2 in df_aux2.iterrows():
        if row['Neoplasms benign, malignant and unspecified (incl cysts and polyps)'] == row2['smiles']: #smile-smile
            category = row2['drug'] #root
            print(category)
            try:
                #index_of_category = row.columns.get_loc(category)
                if category in list_meddras:
                    row[category] = 1
                    row['Neoplasms benign, malignant and unspecified (incl cysts and polyps)'] = row2['smiles']
                    
                else:
                    print('nao pertence à lista')
            except:
                print('erro')
                
        
    
df_final = df_final.fillna(1)
df_final.to_excel('output_final.xlsx', header=True, index=False)

z = df_final.drop_duplicates('smiles')
z.to_csv('output_final75.csv', header=True, index=True)



