import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules
import os
from handler_db import store_results, get_results
import sys


def prepareData(df: pd.DataFrame) -> pd.DataFrame:
    # dropping date column
    df = df.drop(columns=['Date'], axis=1)

    # converts the dataframe to a list of lists
    data = [
        item_list.replace('\"', "").split(",") \
        for item_list in df['items']
    ]
    # for row in range(len(df)):
        # data.append([str(x) for x in df.loc[row,:].values \
            # if str(x) != 'None' and str(x) != 'nan'])
    te = TransactionEncoder()
    te_ary = te.fit(data).transform(data)
    
    return pd.DataFrame(te_ary, columns=te.columns_)


def run_apriori(id, filepath, support) -> pd.DataFrame:
    # file_extension = os.path.splitext(filepath)[1][1:]
    # # print(file_extension)
    #if file_extension == 'csv':
    #    df = pd.read_csv(filepath)
    #elif file_extension == 'xlsx' or file_extension == 'xls':
    #    df = pd.read_excel(filepath)
    #else:
    #    return None

    # MIN_SUP_DEFAULT = 0.1

    df = pd.read_csv(filepath)
    freq_itemsets = apriori(
            prepareData(df), 
            min_support=support, 
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


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Usage: python3 apriori-script.py <path-to-dataset> <uuid> <min-support>")
        exit(1)

    FILEPATH = str(sys.argv[1])
    ID = str(sys.argv[2])
    sup = float(sys.argv[3])
    
    run_apriori(ID, FILEPATH, sup)
