#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 17 00:10:28 2019

@author: angelabarros
"""

import urllib.request, urllib.error, urllib.parse
import json
import os
import pandas as pd
import csv

REST_URL = "http://data.bioontology.org"
API_KEY = "apikey token=f05c3f4e-584c-4e76-a4a9-0ee3e8fccc5c"

data = pd.read_csv("offsides_socs.csv", sep=',' ,error_bad_lines=False) 
data


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
df = data.loc[:,['CUI','SOC']]

combined = data.loc[:,['umls_id','drug']]



df = df.head(200)
combined = combined.head(200)



for index,row in df.iterrows():
   #print(row['CUI'])
   for index2, row2 in combined.iterrows():
       if(row['CUI'] == row2['umls_id']):
           df_aux2 = pd.DataFrame([[row['CUI'],0,row['SOC'], row2['drug']]], columns={'drug','smiles','SOC', 'CUI'})
           df_aux = df_aux.append(df_aux2,ignore_index=True)
    
import pubchempy as pcp
from pubchempy import get_compounds


for index, row in df_aux.iterrows():
    for compound in get_compounds(row['drug'], 'name'):
        print(compound.cid)
        print(compound.isomeric_smiles)
        df_aux3 = pd.DataFrame([[row['drug'],compound.isomeric_smiles, row['SOC'], row['CUI']]], columns={'CUI','smiles','SOC', 'drug'})
        df_aux2 = df_aux2.append(df_aux3,ignore_index=True)
       
for index, row in df_aux2.iterrows():
    category_meddra = row['SOC']
    smile = row['smiles']
    df_final = df_final.append({'smiles' : smile,'Hepatobiliary disorders' : 0,'Metabolism and nutrition disorders' : 0,
                                 'Product issues' : 0,'Eye disorders' : 0,'Investigations' : 0,
                                 'Musculoskeletal and connective tissue disorders' : 0,
                                 'Gastrointestinal disorders' : 0, 'Social circumstances' : 0,
                                 'Immune system disorders' : 0, 'Reproductive system and breast disorders' : 0,
                                 'Neoplasms benign, malignant and unspecified (incl cysts and polyps)' : 0,
                                 'General disorders and administration site conditions' : 0,
                                 'Endocrine disorders' : 0,'Surgical and medical procedures' : 0,
                                 'Vascular disorders' : 0,'Blood and lymphatic system disorders' : 0,
                                 'Skin and subcutaneous tissue disorders' : 0,'Congenital, familial and genetic disorders' : 0,
                                 'Infections and infestations' : 0, 'Respiratory, thoracic and mediastinal disorders' : 0,
                                 'Psychiatric disorders' : 0, 'Renal and urinary disorders' : 0,
                                 'Pregnancy, puerperium and perinatal conditions' : 0, 'Ear and labyrinth disorders' : 0,
                                 'Cardiac disorders' : 0, 'Nervous system disorders' : 0,
                                 'Injury, poisoning and procedural complications' : 0}, ignore_index = True)



for index, row in df_final.iterrows():
    for index2, row2 in df_aux2.iterrows():
        if row['smiles'] == row2['smiles']: #smile-smile
            category = row2['SOC'] #root
            print(category)
            try:
                #index_of_category = row.columns.get_loc(category)
                if category in list_meddras:
                    print('pertence à lista do meddras')
                    #index[category] = 1
                    df_final.loc[index, category] = 1
                    #df_final[category] = df_final[category].map({category: 1})
                    #row['Congenital, familial and genetic disorders'] = row2['smiles']
                    
                else:
                    print('nao pertence à lista')
            except:
                print('erro')
                
df_final = df_final.fillna(1)
df_final.to_excel('output_final45.xlsx', header=True, index=False)