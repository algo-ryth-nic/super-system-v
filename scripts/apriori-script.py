import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules
import json
from flask import Flask, request, jsonify

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

@app.post('/aprori')
def upload_data():
    data = request.get_json(force=True)

    df = pd.read_json(json.dumps(data), orient='records')
    # make async call to apriori
    freq, rules = apply_apriori(df, 0.02)
    data = {'frequent-itemsets': freq, 'association-rules': rules}
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)


"""
- Instead of taking json as input, take a csv file using post
- on successful upload, return a private url endpoint using UUID
- on calling that endpoint, return an html
- make endpoint for get request for getting freq & rules
- integrate mongodb to the script
- make call to aprori async, on completion store that in a document with UUID as an id
- change the input form of table, extra processing
"""