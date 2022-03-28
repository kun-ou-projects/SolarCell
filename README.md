Authors: Satanu Ghosh and Dr. Kun Lu

# Band Gap Information Extraction from Material Science Literature

## data_download.py
 
 This script uses the list of dois mentioned in Tshitoyan et al. (2019) (https://www.nature.com/articles/s41586-019-1335-8). Using this script we curated our first set of 1.44 million title + abstract.
 
 ## dataset_creation.py
 
 We used some filteration methods to filter title and abstracts from the dataset that are only relevant to our work. Doing this we reduce the usable dataset to ~12000 instances
 
 ## doc_access.py
 
 The driver class of the entire system that iterates over the dataset and also post-process on the output to only store information about material whose band gap value has been successfully extracted while ignoring the other information.
 
 ## band_gap.py
 
 The elements of the band gap parser and their properties are declared here and works as a new data structure that we use in band_gap_parser.py
 
 ## band_gap_parser.py
 
 In this script we describe the structure of the Band Gap parser, extract information from the parse tree, and relate it to the Compound Parser. The final record of information is initialized here.
 
 ## parser_grammar.py
 
 This script contains all the different regex grammars we used to identify a piece of text as bang gap value or specifier. Information extraction to construct the parse tree is being done here.
 
## extract_bg.py

This file is the first consolidated version of the code
 
 
