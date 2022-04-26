import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os

def prepareData(df: pd.DataFrame) -> pd.DataFrame:
    # converts the dataframe to a list of lists
    data = []
    for row in range(len(df)):
        data.append([str(x) for x in df.loc[row,:].values \
            if str(x) != 'None' and str(x) != 'nan'])
    te = TransactionEncoder()
    te_ary = te.fit(data).transform(data)
    
    return pd.DataFrame(te_ary, columns=te.columns_)


def apply_apriori(data: pd.DataFrame, min_sup: float) -> pd.DataFrame:
    freq_itemsets = apriori(prepareData(data), min_support=min_sup, use_colnames=True).sort_values(by='support', ascending=False)
    rules= association_rules(freq_itemsets, metric="lift", min_threshold=1).sort_values(by=['lift', 'confidence'], ascending=False)


    json_freq_items, json_rules = freq_itemsets.to_json(orient='records'), \
        rules.to_json(orient='records')
    return json_freq_items, json_rules



# flask setup
app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
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
        # to prevent modification of server's filesystem
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # saves the file 
        file.save(file_path)
        if os.path.exists(file_path):
            return jsonify({"message" : "upload succesful!"}), 201
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
    app.run(debug=True)


"""
- Add a file size limit
"""