from chemdataextractor import Document
from chemdataextractor.doc import Heading, Paragraph, Title
from chemdataextractor.model import BaseModel, StringType, ListType, ModelType
from chemdataextractor.model import Compound
from lxml import etree
from chemdataextractor.parse import R, I, W, T, Optional, merge, join, Any, OneOrMore, Not, ZeroOrMore, SkipTo
from chemdataextractor.parse.base import BaseParser
from chemdataextractor.parse.common import lbrct, dt, rbrct, comma
from chemdataextractor.utils import first
from chemdataextractor.parse.cem import cem, chemical_label, lenient_chemical_label, solvent_name, CompoundParser, \
    ChemicalLabelParser
from parser_grammar import *
from band_gap import *

bg = (mcem_cem_prefix_value
         | value_prefix_cem
         | cem_value_prefix
         | cem_prefix_value
         | prefix_cem_value
         | prefix_value_cem)

class BandgapParser(BaseParser):
    root = bg

    def interpret(self, result, start, end):
        #print(etree.tostring(result))
        #print(result.xpath('./specifier/text()'))
        raw_value = first(result.xpath('./evolt/value/text()'))
        raw_units = first(result.xpath('./evolt/units/text()'))
        try:
            specifier = ' '.join(
                [i for i in (first(result.xpath('./specifier'))).itertext()])
        except BaseException:
            specifier = ''

        #understanding

        band_gap = Compound(
            band_gaps=[
                BandGap(
                    raw_value=raw_value,
                    raw_units=raw_units,
                    specifier=specifier,
                )
            ]
        )
        # find chemical entity mentions in this matched result
        cem_el = first(result.xpath('./cem'))
        #print(cem_el)
        if cem_el is not None:
            band_gap.names = cem_el.xpath('./cem/name/text()')
            band_gap.labels = cem_el.xpath('./cem/label/text()')
        yield band_gap


Paragraph.parsers = [CompoundParser(), BandgapParser()]


# d = Document(
#    Heading(u'''Thickness dependence of structural, optical and luminescence properties of BaTiO3 thin films prepared
#     by RF magnetron sputtering'''),
#     Paragraph(u'''BaTiO 3 thin films were deposited onto quartz substrates by RF magnetron sputtering. X-ray
#     diffraction pattern showed the formation of BT thin films with a tetragonal structure with orientations along (
#     101) plane. Average crystallite size increased from 12.52 to 14.87 nm as the film thickness increased from 207 to
#     554 nm. With the increase in film thickness, the structural disorder decreases and the crystalline quality of the
#     films gradually improved. The film exhibited good adherence to the substrate and are crack free. X-ray
#     photoelectron spectroscopy revealed the presence of barium, titanium and oxygen in BT film. An average
#     transmittance of >80 % was observed for all the films. This high transmittance BT films in the visible region is
#     suitable for various electro-optic applications. The transmittance spectra showed high UV-shielding properties.
#     Optical band gap was found to decrease from 4.55 to 3.70 eV with increase of film thickness, whereas the
#     refractive index was found to increase. The refractive index of the BT films can be tuned between 2.11 and 2.21
#     at 550 nm. The real and imaginary dielectric constants with increase in film thickness were investigated. The low
#     dissipation factor of BT thin films makes it a promising material for frequency agile applications. The emission
#     spectra of BT thin films consist of near band edge excitonic UV emission and defect related emission in the
#     visible range. The PL emission bands in UV and visible region of BT thin films make them suitable for
#     electro-optic devices and light emitters.''')
# )
#
# print(d.records.serialize())
