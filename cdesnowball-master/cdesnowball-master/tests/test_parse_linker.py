from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import logging
import re

from chemdataextractor.doc import Document
from chemdataextractor.model import Compound
from chemdataextractor.doc import Paragraph, Heading

from chemdataextractor.parse.cem import cem, chemical_label, lenient_chemical_label, solvent_name
from chemdataextractor.parse.common import lbrct, dt, rbrct
from chemdataextractor.utils import first
from chemdataextractor.model import Compound
from chemdataextractor.parse.actions import merge, join
from chemdataextractor.parse.base import BaseParser
from chemdataextractor.parse.elements import W, I, R, Optional, Any, OneOrMore, Not, ZeroOrMore

#It's only extracting the names so how do I change this?
a = Document(
    Paragraph(u' The precipitated solids were filtered off and repeatedly washed with hot methanol \
              and then dried in a vacuum oven at 100 °C to give the pure organic \
              linker 5,5′-((3′,5′-dicarboxy-[1,1′-biphenyl]-3,5-dicarbonyl)bis(azanediyl))diisophthalic acid (H6DBDBD)\
              as a white solid (0.52 g, 77.8% yield)')
)
print(a.records.serialize())

b = Document(
    Paragraph(u'31P NMR (D2O, 121.5 MHz): δ −6.56 (d, 1P, JP,P = 21.9 Hz), −9.89 (d, 1P, JP,P = 21.9 Hz).')
)

print(b.records.serialize())