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


data = pd.read_csv("offsides.csv", sep=';' ,error_bad_lines=False) 
data

cuis = data["umls_id"]

df = pd.DataFrame(columns={'CUI','ROOT'})

def get_json(url):
    opener = urllib.request.build_opener()
    opener.addheaders = [('Authorization', API_KEY)]
    return json.loads(opener.open(url).read().decode('utf-8'))

#teste = cuis.head(2)

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
        print("get_json do CUI"+item+ " deu erro")
    
    
df.to_excel('output.xlsx', header=True, index=False)
    