import sqlite3
import pandas as pd
from chemdataextractor import Document
from chemdataextractor.doc import Heading, Paragraph, Title
from bandgap_parser import *
from chemdataextractor.nlp.tokenize import ChemWordTokenizer
cwt = ChemWordTokenizer()


dataset_path = "C:/Users/satan/PycharmProjects/SolarCell/data/manual_evaluation_dataset.csv"
dataset = pd.read_csv(dataset_path)
#print(dataset.columns)
op_file = open("data/output_changes.txt", 'a', encoding="utf-8")

df = pd.DataFrame(columns = ['doi','publication_date', 'source', 'journal', 'title', 'abstract', 'info_extracted'])
doi = []
paragraph = []
heading = []
source = []
pub_date = []
journal = []
ie = []

for index, row in dataset.iterrows():
    cem_bg_info = []
    heading.append(row['title'])
    paragraph.append(row['abstract'])
    doi.append(row['doi'])
    source.append(row['source'])
    pub_date.append(row['pub_date'])
    journal.append(row['journal'])

    title = row['title']
    abs = row['abstract']
    #print("\nThis is the abstract: "+ paragraph)
    d = Document(
        Heading(title),
        Paragraph(abs)
    )
    record = d.records.serialize()

    for i in record:
        if len(i) > 1:
            cem_bg_info.append(i)

    ie.append(cem_bg_info)

    print(index)

df['doi']=doi
df['publication_date'] = pub_date
df['source'] = source
df['journal'] = journal
df['title'] = heading
df['abstract'] = paragraph
df['info_extracted'] = ie


df.to_csv("data/manual_eval_with_context_ie.csv")
# d1 = Document(
#     #Heading(u'''Relation between interface states and temperature behavior of the barrier height of silver contacts on clean cleaved n-type silicon '''),
#     Paragraph(u'''The temperature dependence of the indirect band gap for each direction
#     of light polarization is linear with a slope of -4·05 × 10−3eV and -4·37 × 10−3eV respectively.
#
# .
# ''')
#     )
#
# #paragraph = u'''In this work, we present a facile method without hazardous material for improving the liquid-phase exfoliation of MoS2 nanosheets by use of pre-freezing and thermal shock. The MoS2 bulk is easily exfoliated and functionalized by prefreezing and thermal shock of MoS2 powder in the ethanol solvent. Atomic force microscopy confirms that the approach can exfoliate MoS2 powder to nanosheets. UV–visible spectroscopy of the prepared samples shows that fingerprint excitonic peaks appear in the spectrums and they become sharper by repeating the process. Optical band gap from Tauc plot of UV–visible spectrum shows an increase in the band gap of exfoliated MoS2 up to 1.85eV and the surface energy of the exfoliated MoS2 is measured as 29.8mJ/m2. Annealing the prepared samples at temperatures up to 400°C decreases the contact angle of water droplet from 130° down to 2°. X-ray diffraction patterns and Fourier transform infrared spectroscopy confirm that exfoliated MoS2 is functionalized during the exfoliation process and molybdite is formed on the surface by crumpling and agglomerating nanosheets due to heating, which is mainly responsible for increasing the surface energy as well as superhydrophilicity of the samples at 400°C..
# #'''
# #parsed = d1.records.serialize()
# #print(type(d1.paragraphs[0].sentences))
# #sentence = d1.paragraphs[0].sentences
# #print(sentence[0].pos_tagged_tokens)
# #print(parsed)
#
# d2 = Document(
#      Heading(u'''Optical absorption edge in SnS '''),
#      Paragraph(u'''The direct band gap of Cu2ZnSnS4 is estimated to be about 1.5 eV
#
# ''')
#      )
#
# d3 = Document(
#     Heading(u'''Optical absorption edge in SnS '''),
#      Paragraph(u'''From an analysis of the data, indirect band gaps of
#      1.142 eV and 1.095 eV were found for the two directions of polarization.''')
# )
# #print(d2.records())
# print(d3.records.serialize())
#tokenized = cwt.tokenize(paragraph)
# #print(tokenized)
#
# #for example generation
# #d3 = Document(
#     #Heading(u'''A study on characterization of Al/ZnS/p-Si/Al heterojunction diode synthesized by sol–gel technique'''),
# #    Paragraph(u'''The glasses representing (Bi2O3)
# #                        x
# #                     (WO3)
# #                        y
# #                     (TeO2)100−
# #
# #                        x
# #
# #                     −
# #
# #                        y
# #                      and (PbO)
# #                        x
# #                     (WO3)
# #                        y
# #                     (TeO2)100−
# #
# #                        x
# #
# #                     −
# #
# #                        y
# #                      systems were prepared. The dilatometric glass-transition temperatures of examined glass samples were found in the region 383–434°C, the coefficient of thermal expansion varied from 12 to 16ppm/°C and the density ranged from 6.302 to 6.808
# #                     g/cm3. From the optical transmission measurements of thin glassy bulk samples prepared by a glass blowing, the optical gap values were found in the narrow region 3.21–3.36eV. For the temperature interval 300–480K, the values of the temperature coefficient of the optical band gap varied from 3.7×10−4 to 5.24×10−4
# #                     eV/K. It is suggested that Raman feature observed at around 350cm−1 can be assigned to an overlap of Raman bands attributed to WO6 corner shared octahedra and to the following three atomic linkages: Bi–O–Te, Pb–O–Te and W–O–Te.''')
# #)
# #print(d3.paragraphs[0].sentences)
# #print(d3.paragraphs[0].sentences[len(d3.paragraphs[0].sentences)-3])
# #print(d3.paragraphs[0].sentences[len(d3.paragraphs[0].sentences)-3].tokens)
# #print(d3.paragraphs[0].sentences[len(d3.paragraphs[0].sentences)-3].pos_tagged_tokens)
# #print(d3.paragraphs[0].sentences[len(d3.paragraphs[0].sentences)-3].ner_tagged_tokens)
# #print(d3.paragraphs[0].sentences[len(d3.paragraphs[0].sentences)-3].tagged_tokens)
# #print(d3.paragraphs[0].sentences[len(d3.paragraphs[0].sentences)-1].records)
# #print("\n"+str(d3.paragraphs[0].sentences[len(d3.paragraphs[0].sentences)-3].records.serialize()))
# #print(d3.paragraphs[0].sentences[len(d3.paragraphs[0].sentences)-3].context)
#
# #print(d3.records.serialize())
# #print(d3.paragraphs[0].tokens)
