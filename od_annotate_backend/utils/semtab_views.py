from django.utils.translation import ugettext as _
from django.conf import settings
import numpy as np
import pandas as pd
import os, time
import json
import math
import decimal
import random
import string
import pandas as pd
import logging
import io
import requests
import re
from semtab.application.utils.MtabExtractTable import MtabAnnotationApi
from semtab.application.utils.utils import printDf, executeSparqlQuery, insertColumnDf, writeHtmlFile

#remove numerical and geographical columns from df before using it
#take only the MAX_ROWS_SEMTAB (10) first rows
def process_df(request, df):
    list_columns_toremove = []
    for col in df.columns:
        #Delete numerical columns
        if df[col].dtype.name == 'float64' or df[col].dtype.name == 'int64':
            if not (df[col].dtype.name == 'int64' and checkexists(col)):
                list_columns_toremove.append(col)
        elif df[col].dtype.name == "object":        #Delete geographical columns
           df_notnull = df.dropna(subset=[col])
           if geo_regex(df_notnull,col,0) or geo_regex(df_notnull,col,1):
               list_columns_toremove.append(col)
    if len(list_columns_toremove) > 0:
        df = df.drop(list_columns_toremove, axis=1)

    if df.shape[0] > settings.MAX_ROWS_SEMTAB:
        df = df.iloc[:settings.MAX_ROWS_SEMTAB]

    return df

#Check if the link is downloadable
def is_downloadable(url):
    """
    Does the url contain a downloadable resource
    """
    h = requests.head(url, allow_redirects=True)
    header = h.headers
    content_type = header.get('content-type')
    if 'zip' in content_type.lower():
        return False
    elif 'html' in content_type.lower():
        return False
    content_length = header.get('content-length', 0)
    content_length = int(content_length)
    if content_length and content_length > settings.MAX_UPLOAD_FILE:  # 200 mb approx
        return False
    return True

#Get delimiter of csv file
def detectDelimiter(header, can=False):
    if header.find(";") != -1:
        return ";"
    if header.find(",") != -1:
        return ","
    if can:
        return ""
    #default delimiter (MS Office export)
    return ";"

#Get file name from link
def get_filename_from_cd(cd):
    """
    Get filename from content-disposition
    """
    if not cd:
        return None
    fname = re.findall('filename=(.+)', cd)
    if len(fname) == 0:
        return None
    file_name = fname[0].replace('"', "")
    file_name = file_name.replace("'", "")
    return file_name

#test regex for geo point and geo shape
def geo_regex(df, col, type=0):
    result = False
    if df is None:
        return result
    reg_geo_point = "(-?\d+(\.\d+)?),\s*(-?\d+(\.\d+)?)"
    nb_rows = int(df.shape[0])
    nb_test = 0
    nbtotal_test = 0
    if type == 0 and df[col].dtype.name == "object": #geo_point
        for i in range(2):
            if nb_rows > i:
                nbtotal_test = nbtotal_test + 1
                val = df.at[i,col]
                val = val.lower()
                if re.search(reg_geo_point, val):
                    nb_test = nb_test + 1
        #print(col+"========="+str(nbtotal_test)+"========"+str(nb_test))
        if nb_test == nbtotal_test:
            result = True
    elif type == 1 and df[col].dtype.name == "object": # geo_shape
        for i in range(2):
            if nb_rows > i:
                nbtotal_test = nbtotal_test + 1
                val = df.at[i,col]
                val = val.lower()
                if re.search(reg_geo_point, val) and (re.search("type", val) or re.search("polygon", val) or re.search("coordinates", val)):
                    nb_test = nb_test + 1
        #print(col+"========="+str(nbtotal_test)+"========"+str(nb_test))
        if nb_test == nbtotal_test:
            result = True
    return result

#Save file link to path with extension .csv
def save_upload_file(request, file_link, file_ext=".csv"):
    df = None
    is_local = True
    filename = ""
    full_filename = ""
    if "http" in file_link:
        is_local = False
        if not is_downloadable(file_link):
            return full_filename, filename
        r = requests.get(file_link, allow_redirects=True)
        content = r.content
        if not content or content is None:
            return full_filename, filename
        file_link = io.StringIO(content.decode('utf-8'))

        filename = get_filename_from_cd(r.headers.get('content-disposition'))
        file_ext = filename.split(".")[-1]
        file_ext = "."+file_ext
    elif "\/" in file_link or "\\" in file_link:
        file_link = file_link
    else:
        file_link = settings.SEMTAB_FILES+file_link

    if (file_ext).lower() == ".csv":
        if is_local:
            with open(file_link, 'r', encoding='utf-8') as myCsvfile:
                header=myCsvfile.readline()
            separator=detectDelimiter(header)
        else:
            for header in file_link.getvalue().split('\n'):
                separator=detectDelimiter(header)
                break
        df = pd.read_csv(file_link, sep=separator, encoding='utf8')
    elif (file_ext).lower() == ".json":
        df = pd.read_json(file_link, encoding='utf8')
    elif (file_ext).lower() == ".xls" or (file_ext).lower() == ".xlsx":
        df = pd.read_excel(file_link, 0)

    if df is not None:
        df = process_df(request,df)

        filename = ''.join(random.choice(string.ascii_lowercase) for i in range(16))
        full_filename = settings.SEMTAB_FILES + filename + '.csv'
        df.to_csv(full_filename, index = False)

    return full_filename, filename

#Annotate the table
def annotate_table(request, file_link, file_ext=".csv"):
    full_filename, filename = save_upload_file(request, file_link, file_ext)
    request.session['semtab_file'] = filename
    html = ""
    #df = None
    graph_json = ""
    graph_json_full = ""
    subjectColumnId = ""

    final_col = []
    final_cta = []
    final_cpa = []
    final_cea = []

    if full_filename != "":
        files = [full_filename]

        api = MtabAnnotationApi(files)
        api.extractTableHTML()

        cea = api.getList_CEA_Global()
        final_col = cea[0].pop(0)
        final_cea = cea[0]
        print("=====================================CEA")
        print(final_cea)

        cpa = api.getList_CPA_Global()
        final_cpa = cpa[0]
        print("=====================================CPA")
        print(final_cpa)

        cta = api.getList_CTA_Global()
        cta[0].pop(0)
        final_cta = cta[0]
        print("=====================================CTA")
        # Pour chaque CTA, le premier index est nul. Je l'ai enlevé dans le for juste en dessous.
        print(final_cta)

        """numberOfDf = len(cpa)
        listDf = list()

        for i in range(0, numberOfDf, 1):
            df = pd.DataFrame(data=cea[i],
                                   columns=cpa[i],
                                   dtype=str)
            #Supprime la premiere ligne du fichier en ajustant les indexes
            df = df.reindex(df.index.drop(0)).reset_index(drop=True)
            cta[i].pop(0)
            listCol = df.columns.values.tolist()
            #Supprime les colonnes qui n'ont pas été trouvées par Mtab
            if "" in listCol:
                df.drop(labels=[""], axis=1, inplace=True)
            #Supprime les colonnes dupliquées
            df = df.loc[:, ~df.columns.duplicated()]
            #Affiche le tableau
            print("=====================================print final result")
            print(df)
            #html = df.to_html(classes='table table-striped text-center', justify='center')
            #printDf(df)
            listDf.append(df)"""

        html = api.getAnnotated_table_Global()

        graph_json, graph_json_full, subjectColumnId = generate_graph(request, final_col, final_cta, final_cpa, final_cea)

    return {"html": html, "graph_json": graph_json, "graph_json_full": graph_json_full, "subjectColumnId": subjectColumnId}

#Generate graph from dataframe and save it
def generate_graph(request, final_col, final_cta, final_cpa, final_cea):
    path_filename = settings.SEMTAB_FILES + request.session['semtab_file'] + '.json'
    path_filename_full = settings.SEMTAB_FILES + request.session['semtab_file'] + '_full.json'
    subjectColumnId = writeHtmlFile(final_col, final_cta, final_cpa, final_cea, path_filename, path_filename_full)
    graph_path = settings.SEMTAB_GRAPH_URL + request.session['semtab_file'] + '.json'
    graph_path_full = settings.SEMTAB_GRAPH_URL + request.session['semtab_file'] + '_full.json'
    return graph_path, graph_path_full, subjectColumnId

def checkexists(search):
    for val in settings.NUM_TO_NOT_REMOVE:
        if val in search.lower():
            return True
    return False
