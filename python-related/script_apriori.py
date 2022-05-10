import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules
import numpy as np
from handler_db import store_results
import sys


def prepareData(df: pd.DataFrame) -> pd.DataFrame:
    # dropping date column
    df = df.drop(columns=['Date'], axis=1)

    # converts the dataframe to a list of lists
    data = [
        item_list.replace('\"', "").split(",") \
        for item_list in df['items']
    ]
   
    te = TransactionEncoder()
    te_ary = te.fit(data).transform(data)
    
    return pd.DataFrame(te_ary, columns=te.columns_)


def extract_rules(generate_rules: pd.DataFrame) -> pd.DataFrame:
    rules = generate_rules.copy()
    rules['temp'] = [rules['antecedents'].iloc[i].union(rules['consequents'].iloc[i]) \
        for i in range(0,len(rules)) ]
    rules.drop_duplicates(subset=['temp'])
    rules.drop('temp', axis = 1, inplace = True)

    return rules


def run_apriori(id, data, support) -> pd.DataFrame:
    df = data.copy()
    freq_itemsets = apriori(
            prepareData(df), 
            min_support=support, 
            use_colnames=True
        ).sort_values(by='support', ascending=False)


    if len(freq_itemsets) == 0:
        print(f"[!] No frequent itemsets found with support {support}!")
        return False

    rules= association_rules(
            freq_itemsets, 
            metric="lift", 
            min_threshold=1
        ).sort_values(by=['lift', 'confidence'], ascending=False)

    extracted_rules = extract_rules(rules)
    
    print(f"[>] Generated... {len(extracted_rules)} rules!")

    json_freq_items, json_rules = freq_itemsets.to_json(orient='records'), \
        extracted_rules.to_json(orient='records')

    results = {
        "freq_items": json_freq_items,
        "rules": json_rules
    }
    
    # stores results 
    store_results(id, results)

    return json_freq_items, json_rules


def support_generator(items,attempts=10):
    # using an avg-sup value as a starting point for reducing search space
    # calculated by taking the 
    # total no. transactions / sum of total number of items per transaction
    starting_sup = len(items)/sum([len(i.split(',')) for i in items])

    for sup in np.linspace(starting_sup, 0.01, attempts):
        yield sup


if __name__ == '__main__':
    print("Running script_apriori.py")
    if len(sys.argv) < 4:
        print("Usage: python3 apriori-script.py <path-to-dataset> <uuid> <min-support>")
        exit(1)

    FILEPATH = str(sys.argv[1])
    ID = str(sys.argv[2])
    sup = float(sys.argv[3])
    
    df = pd.read_csv(FILEPATH)
    
    sup_gen = support_generator(df['items'])

    # on first run, if failed... brute force on various sup values 
    while not run_apriori(ID, df, sup):
        try: 
            new_sup = next(sup_gen)
            sup = new_sup
            print(f"[!] Retrying with a different support value => {sup}")    
        except StopIteration:
            raise Exception("No more support values to try")
