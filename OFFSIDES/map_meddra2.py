import json
import pandas as pd
import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter


REST_URL = "http://data.bioontology.org"
API_KEY = "70d0c0ad-f6be-48e2-9241-8d987f4d1037"

s = requests.Session()
s.headers.update({"Authorization": "apikey token=70d0c0ad-f6be-48e2-9241-8d987f4d1037"})
retries = Retry(total=15,
                backoff_factor=0.1,
                status_forcelist=[ 500, 502, 503, 504 ])
s.mount('http://', HTTPAdapter(max_retries=retries))


from_json = json.JSONDecoder().decode


def validate_response(response, raw=False):
    if response.ok:
        if raw:
            return response
        else:
            return response.content
    else:
        response.raise_for_status()


def http_get(url, params=None, stream=False):
    response = s.get(url, params=params, stream=stream)
    return validate_response(response, stream)


def get_parent(collection):
    links = collection[0].get("links")
    parents_json = from_json(str(http_get(links.get("parents")).decode('utf-8')))
    if len(parents_json) == 0:
        soc = collection[0].get("prefLabel")
        return soc
    else:
        return get_parent(parents_json)


def get_mps(mps_id):
    mps_url = REST_URL + "/search?q=%s&ontologies=MEDDRA&include=prefLabel,properties" % mps_id
    mps_json = from_json(str(http_get(mps_url).decode('utf-8')))
    soc = mps_json.get("collection")[0].get("prefLabel")
    return soc


def get_soc(event_json):
    collection = event_json.get("collection")

    if len(collection) > 0:
        x = collection[0]
        y = x.get("properties")
        # for key in y.keys():
        #     print(key)
        if "http://purl.bioontology.org/ontology/MEDDRA/MPS" in y:
            # if we're at level 4 (= MedDRA Preferred Term) we're able to get MedDRA MPS (MedDRA Preferred System Organ Class) directly
            soc_id = y["http://purl.bioontology.org/ontology/MEDDRA/MPS"][0]
            soc = get_mps(soc_id)
            # "http://data.bioontology.org/search?q=10037175&ontology=MEDDRA" get_json failed for this one but it exists. increase retries??

        elif "http://purl.bioontology.org/ontology/MEDDRA/classified_as" in y: # i think only level 5 (LLT) terms have this property
            # event is a level 5 term (= MedDRA Lowest Level Term). to get MPS we need to get to level 4
            # can't use parents for level 5 terms because it returns an empty list for some reason
            # using "classifiedAs" instead to get to level 4

            level4_id = y["http://purl.bioontology.org/ontology/MEDDRA/classified_as"][0].split("/")[-1]
            level4_url = REST_URL + "/search?q=%s&ontologies=MEDDRA&include=properties" % level4_id
            level4_json = from_json(str(http_get(level4_url).decode('utf-8')))
            z = level4_json.get("collection")[0].get("properties")
            soc_id = z["http://purl.bioontology.org/ontology/MEDDRA/MPS"][0]
            soc = get_mps(soc_id)

        else: # Neither level 4 nor 5
            soc = get_parent(collection)

    else:
        print("Unable to get System Organ Class")
        soc = ""

    return soc


def preprocess_data2(filepath, output_file):
    data = pd.read_csv(filepath, sep='\t', header=0)
    print(data.columns.values)
    # cuis = data.drop_duplicates(subset="umls_id")["umls_id"] # offsides
    cuis = data.drop_duplicates(subset="event_umls_id")["event_umls_id"] # twosides

    df = pd.DataFrame(columns=['CUI', 'SOC'])

    for item in cuis:

        search_url = REST_URL + "/search?cui=%s&ontologies=MEDDRA&include=prefLabel,cui,properties" % item

        try:
            search_results = from_json(str(http_get(search_url).decode('utf-8')))
        except:
            soc = ""
            print("Unable to get json for UMLS CUI: '%s'" % item)
        else:
            if len(search_results.get("collection")) == 0:
                soc = ""
                print("CUI doesn't exist in MedDRA")
            else:
                soc = get_soc(search_results)

        df2 = pd.DataFrame([[item, soc]], columns=['CUI', 'SOC'])
        print(df2)
        df = df.append(df2, ignore_index=True)

    # need to merge df with data to map the entire dataset
    # data_mapped = data.merge(df, how="left", left_on="umls_id", right_on="CUI")  # offsides
    data_mapped = data.merge(df, how="left", left_on="event_umls_id", right_on="CUI")  # twosides
    data_mapped.to_csv(output_file, index=False)

preprocess_data2(filepath="3003377s-offsides.tsv", output_file="offsides_socs.csv")
#preprocess_data2(filepath="3003377s-twosides.tsv", output_file="twosides_socs.csv")
