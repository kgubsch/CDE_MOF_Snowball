# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 18:11:22 2021

@author: Kristian
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import logging
import unittest

from lxml import etree

from chemdataextractor.doc.text import Sentence
from chemdataextractor.parse.topology import tp_phrase



logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

class TestParseTopology(unittest.TestCase):
    
    maxDiff = None
    
    def do_parse(self, input, expected):
        s = Sentence(input)
        log.debug(s)
        log.debug(s.tagged_tokens)
        result = next(tp_phrase.scan(s.tagged_tokens))[0]
        log.debug(etree.tostring(result, pretty_print=True, encoding='unicode'))
        self.assertEqual(expected, etree.tostring(result, encoding='unicode'))


    def test_tp1(self):
        s = 'with a defective pcu topology'
        expected = '<top_phrase><tp><abrv>pcu</abrv></tp></top_phrase>'
        self.do_parse(s, expected)
        
if __name__ == '__main__':
    unittest.main()