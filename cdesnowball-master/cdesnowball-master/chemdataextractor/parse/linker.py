from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import logging
import re

from chemdataextractor.parse.cem import cem, chemical_label, lenient_chemical_label, solvent_name
from chemdataextractor.parse.common import lbrct, dt, rbrct
from chemdataextractor.utils import first
from chemdataextractor.model import Compound
from chemdataextractor.parse.actions import merge, join
from chemdataextractor.parse.base import BaseParser
from chemdataextractor.parse.elements import W, I, R, Optional, Any, OneOrMore, Not, ZeroOrMore
from chemdataextractor.model import LinkerYield

units = (R(u'^[$%]$'))('units').add_action(merge)
identifier = I(u'linker').hide()
linker = ((cem))(u'linker').add_action(merge)
abrv = (Optional(lbrct) + I(u'H6DBDBD') + Optional(rbrct))(u'abrv').add_action(merge)
yield_value = (Optional(lbrct) + R(u'^\d+(\.\d+)?$') + Optional(rbrct))(u'yield_value').add_action(merge)
delim = R('^[:;\.,]$')
prefix = (I('yield') | I('of') | R('^,$')).hide()
ly = (prefix + yield_value + units)(u'ly')

bracket_any = lbrct + OneOrMore(Not(ly) + Not(rbrct) + Any()) + rbrct
cem_ly_phrase = (Optional(cem) + Optional(chemical_label) + Optional(lenient_chemical_label) + Optional(I('having')).hide() + Optional(delim).hide() + Optional(bracket_any).hide() + Optional(delim).hide() + Optional(lbrct) + ly + Optional(rbrct))('top_phrase')
to_give_ly_phrase = (Optional((I('defective') + I('to') + (I('give') | I('afford') | I('yield') | I('obtain')) | I('affording') | I('afforded') | I('gave') | I('yielded'))).hide() + Optional(dt).hide() + (cem | chemical_label | lenient_chemical_label) + Optional(ZeroOrMore(Not(ly) + Not(cem) + Any())).hide() + ly)('ly_phrase')
obtained_ly_phrase = ((cem | chemical_label | lenient_chemical_label) + (I('defective') | I('is') | I('are') | I('was')).hide() + Optional((I('afforded') | I('obtained') | I('yielded'))).hide() + Optional(ZeroOrMore(Not(ly) + Not(cem) + Any())).hide() + ly)('ly_phrase')
ly_phrase = cem_ly_phrase | to_give_ly_phrase | obtained_ly_phrase

from chemdataextractor.parse.base import BaseParser
from chemdataextractor.utils import first

class LinkerParser(BaseParser):
    root = ly_phrase

    def interpret(self, result, start, end):
        compound = Compound(
            linkers=[
                LinkerYield(
                    yield_value =first(result.xpath('./ly/yield_value/text()')), #./ means it is searching relative
                    units =first(result.xpath('./ly/units/text()')), #text() selects the text nodes
                )
            ]
        )
        yield compound
        cem_el = first(result.xpath('./cem'))
        if cem_el is not None:
            compound.names = cem_el.xpath('./name/text()')
            compound.labels = cem_el.xpath('./label/text()')
        #else:
        #    raise ValueError('No cem found')
        yield compound
