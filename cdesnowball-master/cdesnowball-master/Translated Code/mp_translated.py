# -*- coding: utf-8 -*-
"""
chemdataextractor.parse.nmr
~~~~~~~~~~~~~~~~~~~~~~~~~~~

NMR text parser.

"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import logging
import re

from chemdataextractor.parse.cem import cem, chemical_label, lenient_chemical_label, solvent_name
from chemdataextractor.parse.common import lbrct, dt, rbrct
from chemdataextractor.utils import first
from chemdataextractor.model import Compound, MeltingPoint
from chemdataextractor.parse.actions import merge, join
from chemdataextractor.parse.base import BaseParser
from chemdataextractor.parse.elements import W, I, R, Optional, Any, OneOrMore, Not, ZeroOrMore

log = logging.getLogger(__name__)

''' __name__ is a special Python variable and it gets its value depending on how we execute the containing script.
when the script is run, the __name__ variable equals __main__ so the when you import the containing script,
it contains the name of the script. Before all other code is run, __name__ is set to __main__. This changes if the 
__name__ variable is imported'''

prefix = Optional(I('a')).hide() + (Optional(lbrct) + W('Tm') + Optional(rbrct)| R('^m\.?pt?\.?$', re.I) | I('melting') + Optional((I('point') | I('temperature')| I('range'))) | R('^m\.?$', re.I) + R('^pt?\.?$', re.I)).hide() + Optional(lbrct + W('Tm') + rbrct) + Optional(W('=') | I('of') | I('was') | I('is') | I('at')).hide() + Optional(I('in') + I('the') + I('range') + Optional(I('of')) | I('about')).hide()

#The prefix variable lays out many possible things preceding the melting point in the text

delim = R('^[:;\.,]$')
'''
R matches the token text to the regular expression
^ matches at start of line any string that contains a : OR ; OR , OR .
$ matches at the end of the line any string that contains a : OR ; OR , OR .
'''


# TODO: Consider allowing degree symbol to be optional. The prefix should be restrictive enough to stop false positives.
units = (W('°') + Optional(R('^[CFK]\.?$')) | W('K\.?'))('units').add_action(merge)

'''
W matches the degree symbol exactly 
Optional means that the unit will be included if it is in the text
R matches the token text to the regular experssion
^ matches any string that contains a C OR F OR K
.add_action(merge) joins the tokens into a single string with no spaces
'''

joined_range = R('^[\+\-–−]?\d+(\.\d+)?[\-–−~∼˜]\d+(\.\d+)?$')('value').add_action(merge)

'''
R matches the token text to the regular experssion
^ matches at beginning of line any string that contains a + - or – or − (they are different apparently)
? matches betweeen zero and one times
\d matches a digit between 0 and 9
+ matches between 1 and unlimited times (greedy)
\. matches . and takes away its special meaning
\-–−~∼˜ matches one of those characters
'''


spaced_range = (R('^[\+\-–−]?\d+(\.\d+)?$') + Optional(units).hide() + (R('^[\-–−~∼˜]$') + R('^[\+\-–−]?\d+(\.\d+)?$') | R('^[\+\-–−]\d+(\.\d+)?$')))('value').add_action(merge)

to_range = (R('^[\+\-–−]?\d+(\.\d+)?$') + Optional(units).hide() + (I('to') + R('^[\+\-–−]?\d+(\.\d+)?$') | R('^[\+\-–−]\d+(\.\d+)?$')))('value').add_action(join)

temp_range = (Optional(R('^[\-–−]$')) + (joined_range | spaced_range | to_range))('value').add_action(merge)

temp_value = (Optional(R('^[~∼˜\<\>]$')) + Optional(R('^[\-–−]$')) + R('^[\+\-–−]?\d+(\.\d+)?$'))('value').add_action(merge)

temp = Optional(lbrct).hide() + (temp_range | temp_value)('value') + Optional(rbrct).hide()

mp = (prefix + Optional(delim).hide() + temp + units)('mp')


bracket_any = lbrct + OneOrMore(Not(mp) + Not(rbrct) + Any()) + rbrct

'''
Brackets. (Note that these could be tagged other than LRB/RRB e.g. as part of CM entity)
lbrct = W('(').hide()
rbrct = W(')').hide()'''

solvent_phrase = (R('^(re)?crystalli[sz](ation|ed)$', re.I) + (I('with') | I('from')) + cem | solvent_name)
cem_mp_phrase = (Optional(solvent_phrase).hide() + Optional(cem) + Optional(I('having')).hide() + Optional(delim).hide() + Optional(bracket_any).hide() + Optional(delim).hide() + Optional(lbrct) + mp + Optional(rbrct))('mp_phrase')
to_give_mp_phrase = ((I('to') + (I('give') | I('afford') | I('yield') | I('obtain')) | I('affording') | I('afforded') | I('gave') | I('yielded')).hide() + Optional(dt).hide() + (cem | chemical_label | lenient_chemical_label) + ZeroOrMore(Not(mp) + Not(cem) + Any()).hide() + mp)('mp_phrase')
obtained_mp_phrase = ((cem | chemical_label) + (I('is') | I('are') | I('was')).hide() + (I('afforded') | I('obtained') | I('yielded')).hide() + ZeroOrMore(Not(mp) + Not(cem) + Any()).hide() + mp)('mp_phrase')

mp_phrase = cem_mp_phrase | to_give_mp_phrase | obtained_mp_phrase

class MpParser(BaseParser):
    """"""
    root = mp_phrase

    def interpret(self, result, start, end):
        compound = Compound(
            melting_points=[
                MeltingPoint(
                    value=first(result.xpath('./mp/value/text()')),
                    units=first(result.xpath('./mp/units/text()'))
                )
            ]
        )
        cem_el = first(result.xpath('./cem'))
        if cem_el is not None:
            compound.names = cem_el.xpath('./name/text()')
            compound.labels = cem_el.xpath('./label/text()')
        yield compound
