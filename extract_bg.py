# This module is modified from ChemDataExtractor battery article code to extract bandgap information It uses
# rule-based extraction
# reference: Huang, S., & Cole, J. M. (2020). A database of battery materials auto-generated
# using ChemDataExtractor. Scientific Data 2020 7:1, 7(1), 1–13. https://doi.org/10.1038/s41597-020-00602-2


# __Author__ = Kun Lu
# Date: Summer 2021


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


# add bandgap model to Compound model
Compound.band_gaps = ListType(ModelType(BandGap))

# define grammars for parser
delim = R(r'^[:;\.,]$')
# define unit grammar, eV
units = (R('^eV$')('units')).add_action(join)

# define various value formatting
joined_range = R(r'^[\+\-–−]?\d+(\.\d+)?(\(\d\))?[\-––-−~∼˜]\d+(\.\d+)?(\(\d\))?$')('value').add_action(join)
spaced_range = (R(r'^[\+\-–−]?\d+(\.\d+)?(\(\d\))?$') + Optional(units).hide() + (R(r'^[\-±–−~∼˜]$') + R(
    r'^[\+\-–−]?\d+(\.\d+)?(\(\d\))?$') | R(r'^[\+\-–−]\d+(\.\d+)?(\(\d\))?$')))('value').add_action(merge)
to_range = (ZeroOrMore(R(r'^[\+\-–−]?\d+(\.\d+)?(\(\d\))?$') + Optional(units).hide()) +
            Optional(I('to')) + R(r'^[\+\-–−]?\d+(\.\d+)?(\(\d\))?$'))('value').add_action(join)
and_range = (Optional(I('between')) +
             ZeroOrMore(R(r'^[\+\-–−]?\d+(\.\d+)?(\(\d\))?$') + Optional(units).hide() +
             Optional(lbrct + ZeroOrMore(R(r'^[^\)]+$')) + rbrct).hide() + Optional(comma)) +
             Optional(I('and') | comma) + R(r'^[\+\-–−]?\d+(\.\d+)?(\(\d\))?$'))('value').add_action(join)
range = (Optional(R(r'^[\-–−]$')) + (and_range | to_range | spaced_range | joined_range)).add_action(merge)
value = (Optional(R(r'^[\-–−]$')) +
         Optional(R(r'^[~∼˜\<\>\≤\≥]$')) +
         Optional(R(r'^[\-\–\–\−±∓⨤⨦±]$')) +
         R(r'^[\+\-–−]?\d+(\.\d+)?(\(\d\))?$')).add_action(join)
ordinal = T('JJ').add_action(join)
power = (Optional((range | value) + R('×')) + (R('10') + W('−') + R(r'\d') | R(r'^10[\-–−]?\d+$'))).add_action(join)
e_volt = (power | range | value | ordinal)('value')  # match ev values

# chemical entity mentions
cem_prefix = (Optional(T('DT')).hide() +
              (cem + Optional(I('doped') + I('with') + cem))('cem') + Optional(I('thin')) +
              Optional(I('film') | I('films')) + Optional(delim).hide())
# multiple chemical entities
multi_cem = ZeroOrMore(cem_prefix + Optional(comma).hide()) + Optional(I('and') | comma).hide() + cem_prefix

# band gap specifier
bg_specifier = (Optional(I('direct') | I('indirect')) +
                Optional(I('electronic') | I('optical')) +
                Optional(I('tunable')) +
                Optional(I('energy')) +
                Optional(I('band')) + Optional(I('-')) +
                (I('Eg') | I('gap') | I('gaps') | I('bandgap') | I('bandgaps')))('specifier')
# specifier prefix
prefix = (
        Optional(I('with')).hide() +
        Optional(I('the') | I('a') | I('an') | I('its')).hide() +
        Optional(I('excellent') | I('high') | I('low') | I('stable') | I('superior') | I('maximum') | I('highest') | I(
            'peak')).hide() +
        bg_specifier +
        Optional(I('energy')).hide() +
        Optional(I('value')).hide() +
        Optional(I('varies') + I('from')).hide() +
        Optional(W('=') | W('~') | W('≈') | W('≃') | I('of') | I('was') | I('is') | I('at') | I('as') | I('near') | I(
            'above') | I('below')).hide() +
        Optional(I('reported') | I('determined') | I('measured') | I('calculated') | I('known')).hide() +
        Optional(I('as') | (I('to') + I('be'))).hide() +
        Optional(I('in') + I('the') + I('range') | I('ranging')).hide() +
        Optional(I('about') | I('from') | I('approximately') | I('around') | (I('high') + I('as')) |
                 (I('higher') | I('lower') + I('than')) |
                 (I('up') + I('to') | I('in') + I('excess') + I('of'))).hide())

# ev value and unit: in the path of ./evolt/value/  and ./evolt/units/
evolt_and_units = (
        Optional(lbrct).hide() +
        e_volt + units +
        Optional(rbrct).hide())('evolt')
evolt_specifier_and_value = Optional(prefix) + (Optional(delim).hide() + Optional(
    lbrct | I('[')).hide() + e_volt + units + Optional(rbrct | I(']')).hide())('evolt')

# define 5 root patterns for evolt_phrase
prefix_cem_value = (
        prefix +
        Optional(multi_cem | cem_prefix | lenient_chemical_label) +
        Optional(lbrct + Optional(cem_prefix | lenient_chemical_label | multi_cem) + rbrct) +
        Optional(I('is') | I('was') | I('were') | I('occurs') | I('of') | I('could') | I('can') | I('remained') | (
                I('can') + I('be') + I('assigned') + Optional(I('at') | I('to')))).hide() +
        Optional(I('reach') | I('reaching') | I('observed') | I('determined') | I('measured') | I('calculated') | I(
            'found') | I('increased') | I('expected') | I('decreases') | I('resulting') | I('estimated')).hide() +
        Optional(
            I('in') + I('the') + I('range') + I('of') | I('ranging') + I('from') | I('as') | I('to') | I('from') | I(
                'to') + I('be') | I('about') | I('over') | (I('higher') | I('lower')) + I('than') | I('above')).hide() +
        Optional(lbrct).hide() + SkipTo((evolt_specifier_and_value | evolt_and_units)) +
        (evolt_specifier_and_value | evolt_and_units) + Optional(rbrct).hide())('evolt_phrase')

cem_prefix_value = ((multi_cem | cem_prefix | lenient_chemical_label)
        + Optional(delim).hide()
        + Optional(I('that') | I('which') | I('was') | I('since') | I('the') | I('resulting') + I('in')).hide()
        + Optional(I('typically') | I('also')).hide()
        + Optional(I('display') | I('displays') | I('presents') | I('exhibit') | I('exhibited') | I('exhibits') | I('exhibiting') |
                   I('shows') | I('show') | I('showed') | I('gave') | I('demonstrate') | I('demonstrates') |
                   I('are') | I('remains') | I('maintains') | I('delivered') | I('provided') | I('undergo') |
                   I('undergoes') | I('has') | I('have') | I('having') | I('determined') | I('with') | I('where') |
                   I('orders') | I('were') | (I('is') + Optional(I('classified') + I('as')))).hide()
        + Optional((I('reported') + I('to') + I('have')) | I('at') | I('with')).hide()
        + Optional(prefix)
        + Optional(lbrct).hide() + (evolt_specifier_and_value | evolt_and_units) + Optional(rbrct).hide()
        + Optional(I('can') + I('be') + I('achieved'))
        )('evolt_phrase')

prefix_value_cem = (
        Optional(I('below') | I('at')).hide() +
        prefix +
        Optional(I('is') | I('were') | I('was') | I('are')).hide() +
        SkipTo((evolt_specifier_and_value | evolt_and_units)) +
        (evolt_specifier_and_value | evolt_and_units) +
        Optional(
            Optional(I('has') + I('been') + I('found')) +
            Optional(I('is') | I('were') | I('was') | I('are')) +
            Optional(I('observed') | I('determined') | I('measured') | I('calculated') | I('reported'))).hide() +
        Optional(evolt_specifier_and_value | evolt_and_units) +
        Optional(I('in') | I('for') | I('of')).hide() +
        Optional(I('the')).hide() +
        Optional(R('^[:;,]$')).hide() +
        Optional(lbrct).hide() +
        Optional(I('of')).hide() +
        SkipTo((multi_cem | cem_prefix | lenient_chemical_label)) +
        (multi_cem | cem_prefix | lenient_chemical_label) +
        Optional(rbrct).hide())('evolt_phrase')

value_prefix_cem = (Optional(I('of')) +
                    (evolt_specifier_and_value | evolt_and_units) +
                    Optional(delim).hide() +
                    Optional(I('which') | I('that')).hide() +
                    Optional(I('has') +
                             I('been') | I('was') | I('is') | I('were')).hide() +
                    Optional(I('found') | I('observed') | I('measured') | I('calculated') | I('determined')).hide() +
                    Optional(I('likely') | I('close') | (I('can') + I('be'))).hide() +
                    Optional(I('corresponds') | I('associated')).hide() +
                    Optional(I('to') + I('be') | I('with') | I('is') | I('as')).hide() +
                    Optional(I('the')).hide() +
                    bg_specifier +
                    Optional(I('of') | I('in')).hide() +
                    (multi_cem | cem_prefix | lenient_chemical_label))('evolt_phrase')

cem_value_prefix = ((multi_cem | cem_prefix | lenient_chemical_label) +
                    Optional((I('is') | I('was') | I('were')) +
                    Optional(I('reported') | I('found') | I('calculate') | I('measured') | I('shown') | I('found')) +
                    Optional(I('to'))).hide() +
                    Optional(I('display') | I('displays') | I('exhibit') | I('exhibits') | I('exhibiting') |
                             I('shows') | I('show') | I('demonstrate') | I('demonstrates') | I('undergo') |
                             I('undergoes') | I('has') | I('have') | I('having') | I('determined') | I('with') |
                             I('where') | I('orders') | (I('is') + Optional(I('classified') + I('as')))).hide() +
                    Optional(I('the') | I('a') | I('an')).hide() +
                    Optional(I('value') | I('values')).hide() +
                    Optional(I('varies') + I('from')).hide() +
                    Optional(W('=') | W('~') | W('≈') | W('≃') | I('was') | I('is') | I('at') | I('as') | I('near') |
                             I('above') | I('below')).hide() +
                    Optional(I('in') + I('the') + I('range') | I('ranging')).hide() +
                    Optional(I('of') | I('about') | I('from') | I('approximately') | I('around') |
                             (I('high') + I('as')) | (I('higher') | I('lower') + I('than'))).hide() +
                    (evolt_specifier_and_value | evolt_and_units) +
                    Optional(I('as') | I('of') | I('for')).hide() +
                    Optional(I('its') | I('their') | I('the')).hide() + bg_specifier)('evolt_phrase')
# multiple cem results in cem, previous mcem hide()
mcem_cem_prefix_value = ((multi_cem | cem_prefix | lenient_chemical_label).hide() + SkipTo(((I('results') | I('result'))
                        + I('in'))) + ((I('results') | I('result')) + I('in')) +
                         (multi_cem | cem_prefix | lenient_chemical_label) + SkipTo(prefix) + prefix +
                         (evolt_specifier_and_value | evolt_and_units)
                         )('evolt_phrase')
# TODO: cem made from/originated from

bg = (mcem_cem_prefix_value
         | value_prefix_cem
         | cem_value_prefix
         | cem_prefix_value
         | prefix_cem_value
         | prefix_value_cem)


# define band gap parser
class BandgapParser(BaseParser):
    root = bg

    def interpret(self, result, start, end):
        #print(etree.tostring(result))
        # print(result.tag)
        raw_value = first(result.xpath('./evolt/value/text()'))
        raw_units = first(result.xpath('./evolt/units/text()'))
        try:
            specifier = ' '.join(
                [i for i in (first(result.xpath('./specifier'))).itertext()])
        except BaseException:
            specifier = ''

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
        if cem_el is not None:
            band_gap.names = cem_el.xpath('./cem/name/text()')
            band_gap.labels = cem_el.xpath('./cem/label/text()')
        yield band_gap


Paragraph.parsers = [CompoundParser(), BandgapParser()]


d = Document(
    Heading(u'''Thickness dependence of structural, optical and luminescence properties of BaTiO3 thin films prepared 
    by RF magnetron sputtering'''),
    Paragraph(u'''BaTiO 3 thin films were deposited onto quartz substrates by RF magnetron sputtering. X-ray 
    diffraction pattern showed the formation of BT thin films with a tetragonal structure with orientations along (
    101) plane. Average crystallite size increased from 12.52 to 14.87 nm as the film thickness increased from 207 to 
    554 nm. With the increase in film thickness, the structural disorder decreases and the crystalline quality of the 
    films gradually improved. The film exhibited good adherence to the substrate and are crack free. X-ray 
    photoelectron spectroscopy revealed the presence of barium, titanium and oxygen in BT film. An average 
    transmittance of >80 % was observed for all the films. This high transmittance BT films in the visible region is 
    suitable for various electro-optic applications. The transmittance spectra showed high UV-shielding properties. 
    Optical band gap was found to decrease from 4.55 to 3.70 eV with increase of film thickness, whereas the 
    refractive index was found to increase. The refractive index of the BT films can be tuned between 2.11 and 2.21 
    at 550 nm. The real and imaginary dielectric constants with increase in film thickness were investigated. The low 
    dissipation factor of BT thin films makes it a promising material for frequency agile applications. The emission 
    spectra of BT thin films consist of near band edge excitonic UV emission and defect related emission in the 
    visible range. The PL emission bands in UV and visible region of BT thin films make them suitable for 
    electro-optic devices and light emitters.''')
)

print(d.records.serialize())
