import sqlite3
import pandas as pd
from chemdataextractor import Document
from chemdataextractor.doc import Heading, Paragraph, Title
from bandgap_parser import *
from chemdataextractor.nlp.tokenize import ChemWordTokenizer
cwt = ChemWordTokenizer()



db_file = "C:/Users/satan/PycharmProjects/SolarCell/data/abstracts.db"

con = sqlite3.connect(db_file)
##abstracts with “band gap” (e.g. “band-gap”, “bandgap”, “band gaps”, “band-gaps”, “bandgaps”), with explicit mentions of “eV”
#df = pd.read_sql_query("Select * from tblAbstract where (abstract like '%band gap%' OR abstract like '%bandgap%' OR abstract like '%band gaps%' OR abstract like '%band-gaps%' OR abstract like '%bandgaps%') AND"
#                       " (abstract like '%eV%' OR abstract like '%electron volt%' OR abstract like '%e-V')", con)
#df = pd.read_sql_query("Select * from tblAbstract where abstract like '%band gap%' OR abstract like '%bandgap%' OR abstract like '%band gaps%' OR abstract like '%band-gaps%' OR abstract like '%bandgaps%' AND abstract like '%eV%' OR abstract like '%electron volt%' OR abstract like '%e-V%'", con)

#sql_command = "Select * from tblAbstract where abstract like ('%band gap%' AND '%eV%') OR abstract like ('%bandgap%' AND '%eV%') OR abstract like ('%band gaps%' AND '%eV%') OR abstract like ('%band-gaps%' AND '%eV%') OR abstract like ('%bandgaps%' AND '%eV%')"
sql_command = "Select * from tblAbstract where abstract like '%band gap%' OR abstract like '%bandgap%' OR abstract like '%band-gap%' OR abstract like '%band gaps%' OR abstract like '%band-gaps%' OR abstract like '%bandgaps%' " \
              "OR title like '%band gap%' OR title like '%bandgap%' OR title like '%band-gap%' OR title like '%band gaps%' OR title like '%band-gaps%' OR title like '%bandgaps%'"
df = pd.read_sql_query(sql_command, con)

#abst = df['abstract']
#print(abst)
print(df.columns)


#df.to_csv("C:/Users/satan/PycharmProjects/SolarCell/data/evaluation_set.csv")
conditioned_dataset = pd.DataFrame()
for index, rows in df.iterrows():
    #print(type(index))
    #print(type(rows))
    item = rows['abstract']
    tokenized = cwt.tokenize(item)
    #print(type(tokenized))
    if 'eV' in tokenized:
        conditioned_dataset=conditioned_dataset.append(rows)



#print(len(conditioned_dataset))
print("Dataset reduced from %d to %d" %(len(df), len(conditioned_dataset)))

manual_evaluation = conditioned_dataset.sample(n=500, random_state=22)
manual_evaluation.to_csv("C:/Users/satan/PycharmProjects/SolarCell/data/manual_evaluation_dataset.csv")
conditioned_dataset.to_csv("C:/Users/satan/PycharmProjects/SolarCell/data/relevant_dataset.csv")
