# -*- coding: utf-8 -*-
"""
Created on Tue Feb 16 08:42:34 2021

@author: Kristian
"""


from chemdataextractor import Document
from chemdataextractor.model import Compound
from chemdataextractor.doc import Paragraph, Heading

#u in front of the string indicates that a unicode string is to be created
#We think the unicode is for symbols like the degree since it may not be recognized ASCII
d = Document(
    Heading(u'Synthesis of 2,4,6-trinitrotoluene (3a)'),
    Paragraph(u'The procedure was followed to yield a pale yellow solid (b.p. 240 °C) and a white solid (b.p. 60 °C)')
)


from chemdataextractor.model import BaseModel, StringType, ListType, ModelType

class BoilingPoint(BaseModel):
    value = StringType()
    units = StringType()
    
Compound.boiling_points = ListType(ModelType(BoilingPoint))

import re
from chemdataextractor.parse import R, I, W, Optional, merge

'''

W = Word
Matches the token text exactly

I = IWord
Case insensitive matching of token text

R = Regex
Matches token text with a regular expression

T= Tag
Matches the tag exactly I think tag refers to POS tag?

H = Hide
Converter for ignoring the results of a parsed expression

'''


'''
R matches the token text to the regular expression
^ matches any string that starts with b
\ removes special meaning from from the . character
? Matches either once or zero times; marks the p as optional
$ Matches at the end of a line
I means the case is not sensitive
| matches either b.p. or boiling point
.hide() I think just makes it so the prefix does not show up in the output but
it still searches the document for the text
'''
prefix = (R(u'^b\.?p\.?$', re.I) | I(u'boiling') + I(u'point')).hide()

'''
W matches the degree symbol exactly 
Optional means that the unit will be included if it is in the text
R matches the token text to the regular experssion
^ matches any string that contains a C OR F OR K
.add_action(merge) joins the tokens into a single string with no spaces
'''

units = (W(u'°') + Optional(R(u'^[CFK]\.?$')))(u'units').add_action(merge)
'''
R matches the token text to a regular experssion
^ matches any string that starts with a digit
\d looks for a number between 0 and 9
+ matches following digits one or more times
\. matches . symbol if it is there
() is the capturing group
? matches the expression zero or one times
'''
value = R(u'^\d+(\.\d+)?$')(u'value')

bp = (prefix + value + units)(u'bp')

from chemdataextractor.parse.base import BaseParser
from chemdataextractor.utils import first

class BpParser(BaseParser):
    root = bp

    def interpret(self, result, start, end):
        compound = Compound(
            boiling_points=[
                BoilingPoint(
                    value=first(result.xpath('./value/text()')),
                    units=first(result.xpath('./units/text()'))
                )
            ]
        )
        yield compound
        
Paragraph.parsers = [BpParser()]

print(d.records.serialize())     


