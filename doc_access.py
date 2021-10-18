import sqlite3
import pandas as pd
from chemdataextractor import Document
from chemdataextractor.doc import Heading, Paragraph, Title
from bandgap_parser import *
from chemdataextractor.nlp.tokenize import ChemWordTokenizer
cwt = ChemWordTokenizer()


dataset_path = "C:/Users/satan/PycharmProjects/SolarCell/data/relevant_dataset.csv"
dataset = pd.read_csv(dataset_path)

# op_file = open("data/output.txt", 'a', encoding="utf-8")
#
# for index, row in dataset.iterrows():
#     heading = row['title']
#     paragraph = row['abstract']
#     #print("\nThis is the abstract: "+ paragraph)
#     d = Document(
#         Heading(heading),
#         Paragraph(paragraph)
#     )
#     record = d.records.serialize()
#     op_file.writelines("\nTitle: \n"+heading+"\n")
#     op_file.writelines("\nAbstract: \n"+paragraph+"\n")
#     op_file.write("\nExtracted Information: \n")
#     for element in record:
#         op_file.write(str(element)+"\n")
#     print(index)
#
# op_file.close()

d1 = Document(
    Heading(u'''Relation between interface states and temperature behavior of the barrier height of silver contacts on clean cleaved n-type silicon '''),
    Paragraph(u'''The properties of silver-silicon interfaces formed by cleaving n-type silicon in ultra high vacuum (UHV) in a stream of evaporating silver atoms were studied. The barrier heights of these contacts were measured at different temperatures by using C-V techniques. All measurements were performed in UHV. The dependence of the barrier height upon temperature did not follow the temperature dependence of the Si band gap as it is usually found. The measured temperature behavior depended on the roughness of the Si surface. The temperature behavior can be explained by assuming a specific band structure of the interface states. For contacts on atomically smooth n-type, the interface states were found to be arranged in two bands, indirect band gap 4 × 10−3 eV wide with acceptor type states 0.18 eV below the intrinsic level E
                     i and a density of 1017 states/cm2 eV, and the other 1 eV wide with donor type states with its upper edge 0.28 eV below E
                     i, and a density of 4 × 1014 states/cm2eV.
.
''')
    )

#paragraph = u'''In this work, we present a facile method without hazardous material for improving the liquid-phase exfoliation of MoS2 nanosheets by use of pre-freezing and thermal shock. The MoS2 bulk is easily exfoliated and functionalized by prefreezing and thermal shock of MoS2 powder in the ethanol solvent. Atomic force microscopy confirms that the approach can exfoliate MoS2 powder to nanosheets. UV–visible spectroscopy of the prepared samples shows that fingerprint excitonic peaks appear in the spectrums and they become sharper by repeating the process. Optical band gap from Tauc plot of UV–visible spectrum shows an increase in the band gap of exfoliated MoS2 up to 1.85eV and the surface energy of the exfoliated MoS2 is measured as 29.8mJ/m2. Annealing the prepared samples at temperatures up to 400°C decreases the contact angle of water droplet from 130° down to 2°. X-ray diffraction patterns and Fourier transform infrared spectroscopy confirm that exfoliated MoS2 is functionalized during the exfoliation process and molybdite is formed on the surface by crumpling and agglomerating nanosheets due to heating, which is mainly responsible for increasing the surface energy as well as superhydrophilicity of the samples at 400°C..
#'''
parsed = d1.records.serialize()
print(type(d1.paragraphs[0].sentences))
sentence = d1.paragraphs[0].sentences
print(sentence[0].pos_tagged_tokens)
#print(parsed)

d2 = Document(
     Heading(u'''Optical absorption edge in SnS '''),
     Paragraph(u'''Optical absorption in single crystals of tin sulfide has been studied at many temperatures between 100 and 300 °K, in the wavelength range 2·2–0·8 μ. From the interference fringe patterns the absorption coefficient, reflection coefficient and index of refraction as a function of wavelength were determined for two light polarizations (ε∥a and ε∥b). From an analysis of the data, indirect band gaps of 1·142 and 1·095 eV were found for the two directions of polarization. Also it was found that the phonon assisted transitions required the participation of two phonons at different energy thresholds with energies 0·033 or 0·038 eV and 0·082 or 0·113 eV, with reference to the two axis. The temperature dependence of the indirect band gap for each direction of light polarization is linear with a slope 4 × 10−3 eV respectively.
''')
     )
#print(d2.records.serialize())
#tokenized = cwt.tokenize(paragraph)
#print(tokenized)




