import sqlite3
import pandas as pd
from chemdataextractor import Document
from chemdataextractor.doc import Heading, Paragraph, Title
from bandgap_parser import *
from chemdataextractor.nlp.tokenize import ChemWordTokenizer
cwt = ChemWordTokenizer()


dataset_path = "data/relevant_dataset.csv"       # dataset to be processed in a csv
dataset = pd.read_csv(dataset_path)              # read in a data frame
df = pd.DataFrame(columns=['doi', 'publication_date', 'source', 'journal', 'title', 'abstract', 'info_extracted'])
doi = []
paragraph = []
heading = []
source = []
pub_date = []
journal = []
ie = []
for index, row in dataset.iterrows():
    cem_bg_info = []                # store extracted information
    heading.append(row['title'])
    paragraph.append(row['abstract'])
    doi.append(row['doi'])
    source.append(row['source'])
    pub_date.append(row['pub_date'])
    journal.append(row['journal'])
    title = row['title']
    abs = row['abstract']
    d = Document(
        Heading(title),
        Paragraph(abs)
    )
    record = d.records.serialize()
    for i in record:
        if "band_gaps" in i.keys():
            cem_bg_info.append(i)
    ie.append(cem_bg_info)
    print(index)
df['doi'] = doi
df['publication_date'] = pub_date
df['source'] = source
df['journal'] = journal
df['title'] = heading
df['abstract'] = paragraph
df['info_extracted'] = ie
df.to_csv("data/information_extracted_dataset.csv")   # write output

