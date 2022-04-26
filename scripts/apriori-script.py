import re
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules
from flask import Flask, request, jsonify
import os
import pymongo
from uuid import uuid4
from datetime import datetime

def prepareData(df: pd.DataFrame) -> pd.DataFrame:
    # converts the dataframe to a list of lists
    data = []
    for row in range(len(df)):
        data.append([str(x) for x in df.loc[row,:].values \
            if str(x) != 'None' and str(x) != 'nan'])
    te = TransactionEncoder()
    te_ary = te.fit(data).transform(data)
    
    return pd.DataFrame(te_ary, columns=te.columns_)


def run_apriori(id, filename) -> pd.DataFrame:
    file_extension = os.path.splitext(filename)[1][1:]
    # print(os.path.splitext(filename))
    # print(file_extension)

    filepath = os.path.join(UPLOAD_FOLDER, filename)
    if file_extension == 'csv':
        df = pd.read_csv(filepath)
    elif file_extension == 'xlsx' or file_extension == 'xls':
        df = pd.read_excel(filepath)
    else:
        return None

    MIN_SUP_DEFAULT = 0.1

    freq_itemsets = apriori(
            prepareData(df), 
            min_support=MIN_SUP_DEFAULT, 
            use_colnames=True
        ).sort_values(by='support', ascending=False)


    rules= association_rules(
            freq_itemsets, 
            metric="lift", 
            min_threshold=1
        ).sort_values(by=['lift', 'confidence'], ascending=False)


    json_freq_items, json_rules = freq_itemsets.to_json(orient='records'), \
        rules.to_json(orient='records')

    results = {
        "freq_items": json_freq_items,
        "rules": json_rules
    }
    
    # stores results 
    store_results(id, results)

    return json_freq_items, json_rules


def store_results(id: str, data: dict):
    # print(data.keys())
    db = connect_to_mongo()
    results = db.apriori_results
    results.insert_one({
        '_id': id,
        'datetime': datetime.now(),
        'frequent_items': data['freq_items'],
        'association-rules': data['rules']
    })


def connect_to_mongo():
    client = pymongo.MongoClient('localhost', 27017)
    db = client.aprioriPlatform
    return db


def get_results(id: str):
    db = connect_to_mongo()
    results = db.apriori_results
    data = results.find_one({'_id': id})
    print(data)
    return data


# flask setup
app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
if not os.path.exists(UPLOAD_FOLDER): os.mkdir(UPLOAD_FOLDER)

ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls', 'txt'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.post('/upload')
def upload_data():
    # check if the post request has the file part
    if 'file' not in request.files:
        return jsonify({"message": "Request has no file part"}), 400
   

    file = request.files['file']
    if file and allowed_file(file.filename):
        id = str(uuid4())
        filename = id + '.' + file.filename.rsplit('.', 1)[1].lower()
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # saves the file 
        file.save(file_path)
        if os.path.exists(file_path):
            return jsonify({"id": id,
            "message" : "upload succesful!"}), 201
        else:
            return jsonify({"message": "something went wrong, couldn't save the file!"}), 500
    else:
        return jsonify({"message" : "File extension not valid, accepted file extensions are " \
            + str(ALLOWED_EXTENSIONS)}), 400


    # data = request.get_json(force=True)

    # df = pd.read_json(json.dumps(data), orient='records')
    # make async call to apriori
    # freq, rules = apply_apriori(df, 0.02)
    # data = {'frequent-itemsets': freq, 'association-rules': rules}
    # return jsonify(data)


if __name__ == "__main__":
    # app.run(debug=True)
    # connect_to_mongo()
    pass

"""
- Add a file size limit
"""