# Authors: Satanu Ghosh and Dr. Kun Lu <br>
## Paper name: <i>Band gap information extraction from materials science literature–a pilot study</i><br>
## Link to paper: https://www.emerald.com/insight/content/doi/10.1108/AJIM-03-2022-0141/full/html

# Pre-requisite:

<ol>
    <li> Create a conda environment for the project using Python 3.8 </li>
    <li> Use the following commands from your anaconda or miniconda prompt to install chemdataextractor:
        <p><code>conda config --add channels conda-forge</code></p>
        <p><code>conda install chemdataextractor</code></p>
   </li>
   <li>dowbload data files for chemdataextractor using:
   <p><code>cde data download</code></p>
   
   </li>
   <li> navigate to chemdataextractor folder in your site-packages, replace the line 445 in chemdataextractor/nlp/tokenize.py with the following code to add tokenization split for eV unit:
   <p><code>QUANTITY_RE = re.compile(r'^((\d\d\d)g|([-−]?\d+\.\d+|10[-−]\d+)(g|s|m|N|V)([-−]?[1-4])?|(\d*[-−]?\d+\.?\d*)([pnµμm]A|[µμmk]g|[kM]J|m[lL]|[nµμm]?M|[nµμmc]m|kN|[emk]V|[mkMG]?W|[mnpμµ]s|Hz|[Mm][Oo][Ll](e|ar)?s?|k?Pa|ppm|min)([-−]?[1-4])?)$')</code></p>
   </li>
   <li>install other requirements</li>
</ol>

# How to run?

<ol>
   <li> Get your Elsevier and Springer API key </li>
   <li> Change the key values in dataset_download.py </li>
   <li> Run dataset_creation.py </li>
   <li> Run doc_access.py
   
</ol>

NOTE: The "data" directory is here with an example file (10 abstracts). Please run the code to populate the data directory.

# Brief description of Python scripts

 ### data_download.py
 
 This script uses the list of dois mentioned in Tshitoyan et al. (2019) (https://www.nature.com/articles/s41586-019-1335-8). Using this script we curated our first set of 1.44 million title + abstract.
 
 ### dataset_creation.py
 
 We used some filteration methods to filter title and abstracts from the dataset that are only relevant to our work. Doing this we reduce the usable dataset to ~12000 instances
 
 ### doc_access.py
 
 The driver class of the entire system that iterates over the dataset and also post-process on the output to only store information about material whose band gap value has been successfully extracted while ignoring the other information.
 
 ### band_gap.py
 
 The elements of the band gap parser and their properties are declared here and works as a new data structure that we use in band_gap_parser.py
 
 ### band_gap_parser.py
 
 In this script we describe the structure of the Band Gap parser, extract information from the parse tree, and relate it to the Compound Parser. The final record of information is initialized here.
 
 ### parser_grammar.py
 
 This script contains all the different regex grammars we used to identify a piece of text as bang gap value or specifier. Information extraction to construct the parse tree is being done here.

