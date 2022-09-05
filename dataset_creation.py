import sqlite3
import pandas as pd
from chemdataextractor import Document
from chemdataextractor.doc import Heading, Paragraph, Title
from bandgap_parser import *
from chemdataextractor.nlp.tokenize import ChemWordTokenizer
cwt = ChemWordTokenizer()



db_file = "data/abstracts.db"

con = sqlite3.connect(db_file)
sql_command = "Select * from tblAbstract where abstract like '%band gap%' OR abstract like '%bandgap%' OR abstract like '%band-gap%' OR abstract like '%band gaps%' OR abstract like '%band-gaps%' OR abstract like '%bandgaps%' " \
              "OR title like '%band gap%' OR title like '%bandgap%' OR title like '%band-gap%' OR title like '%band gaps%' OR title like '%band-gaps%' OR title like '%bandgaps%'"
df = pd.read_sql_query(sql_command, con)

print(df.columns)


conditioned_dataset = pd.DataFrame()
for index, rows in df.iterrows():
    #print(type(index))
    #print(type(rows))
    item = rows['abstract']
    tokenized = cwt.tokenize(item)
    #print(type(tokenized))
    if 'eV' in tokenized:
        conditioned_dataset=conditioned_dataset.append(rows)



print("Dataset reduced from %d to %d" %(len(df), len(conditioned_dataset)))

manual_evaluation = conditioned_dataset.sample(n=500, random_state=22)
manual_evaluation.to_csv("data/manual_evaluation_dataset.csv")
conditioned_dataset.to_csv("data/relevant_dataset.csv")
