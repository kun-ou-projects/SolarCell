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


# define Band gap property model
class BandGap(BaseModel):
    raw_value = StringType()
    raw_units = StringType(contextual=True)
    specifier = StringType(contextual=True)
    understanding = StringType(contextual=True)


# add bandgap model to Compound model
Compound.band_gaps = ListType(ModelType(BandGap))
