import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules
import os
from handler_db import store_results, get_results
from server import UPLOAD_FOLDER

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


if __name__ == "__main__":
    # run_apriori('5c6b8d6b9f8c8a1d8e6d9f2f', 'test.csv')
    print(get_results('787f97e9-c19a-40c7-8853-6fd56bcb475a'))
    pass