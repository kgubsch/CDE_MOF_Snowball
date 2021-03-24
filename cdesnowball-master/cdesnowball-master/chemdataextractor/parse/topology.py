# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 17:49:52 2021

@author: Kristian
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import logging
import re

from chemdataextractor.model import Compound, Topology
from chemdataextractor.doc import Paragraph, Heading

from chemdataextractor.parse.cem import cem, chemical_label, lenient_chemical_label, solvent_name
from chemdataextractor.parse.common import lbrct, dt, rbrct
from chemdataextractor.utils import first
from chemdataextractor.model import Compound
from chemdataextractor.parse.actions import merge, join
from chemdataextractor.parse.base import BaseParser
from chemdataextractor.parse.elements import W, I, R, Optional, Any, OneOrMore, Not, ZeroOrMore

identifier = Optional(I(u'topology')).hide()
topology = (I(u'pcu') | I(u'dia') | I(u'kat') | I(u'SCU') | I(u'tbo') | I(u'dia-a'))(u'abrv').add_action(merge)
full = Optional(I(u'diamondoid'))(u'full') #the string corresponds to the reference below. Still not sure what the syntax
tp = (full + topology + identifier)(u'tp')

import re
from chemdataextractor.parse import R, I, W, Optional, merge
from chemdataextractor.parse.common import lbrct, dt, rbrct
from chemdataextractor.parse.cem import cem, chemical_label, lenient_chemical_label, solvent_name
from chemdataextractor.parse.elements import W, I, R, Optional, Any, OneOrMore, Not, ZeroOrMore

bracket_any = lbrct + OneOrMore(Not(tp) + Not(rbrct) + Any()) + rbrct
delim = R('^[:;\.,]$')
cem_tp_phrase = (Optional(cem) + Optional(chemical_label) + Optional(lenient_chemical_label) + Optional(I('having')).hide() + Optional(delim).hide() + Optional(bracket_any).hide() + Optional(delim).hide() + Optional(lbrct) + tp + Optional(rbrct))('top_phrase')
to_give_tp_phrase = (Optional((I('defective') + I('to') + (I('give') | I('afford') | I('yield') | I('obtain')) | I('affording') | I('afforded') | I('gave') | I('yielded'))).hide() + Optional(dt).hide() + (cem | chemical_label | lenient_chemical_label) + Optional(ZeroOrMore(Not(tp) + Not(cem) + Any())).hide() + tp)('top_phrase')
obtained_tp_phrase = ((cem | chemical_label | lenient_chemical_label) + (I('defective') | I('is') | I('are') | I('was')).hide() + Optional((I('afforded') | I('obtained') | I('yielded'))).hide() + Optional(ZeroOrMore(Not(tp) + Not(cem) + Any())).hide() + tp)('top_phrase')

tp_phrase = cem_tp_phrase | to_give_tp_phrase | obtained_tp_phrase

from chemdataextractor.parse.base import BaseParser
from chemdataextractor.utils import first

class cem_TpParser(BaseParser):
    """"""
    root = tp_phrase

    def interpret(self, result, start, end):
        compound = Compound(
            topologies=[
                Topology(
                    full =first(result.xpath('./tp/full/text()')), #./ means it is searching relative
                    abrv =first(result.xpath('./tp/abrv/text()')) #text() selects the text nodes
                )
            ]
        )
        cem_el = first(result.xpath('./cem'))
        if cem_el is not None:
            compound.names = cem_el.xpath('./name/text()')
            compound.labels = cem_el.xpath('./label/text()')
        yield compound

