import sqlite3
import pandas as pd
from chemdataextractor import Document
from chemdataextractor.doc import Heading, Paragraph, Title
from bandgap_parser import *
from chemdataextractor.nlp.tokenize import ChemWordTokenizer
cwt = ChemWordTokenizer()



db_file = "C:/Users/satan/PycharmProjects/SolarCell/data/abstracts_exp.db"

con = sqlite3.connect(db_file)

df = pd.read_sql_query("Select * from tblAbstract where abstract like '%band gap%' OR abstract like '%bandgap%' OR abstract like '%band gaps%' OR abstract like '%band-gaps%' OR abstract like '%bandgaps%'", con)

count=0
#abst = df['abstract']
#print(abst)
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
        count+=1


print(len(conditioned_dataset))
print(count)

conditioned_dataset.to_csv("C:/Users/satan/PycharmProjects/SolarCell/data/relevant_dataset.csv")