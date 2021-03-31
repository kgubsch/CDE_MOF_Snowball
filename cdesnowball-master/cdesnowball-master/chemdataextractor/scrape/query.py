# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 16:53:21 2021

@author: Kristian
"""


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from abc import abstractmethod
import logging

import requests

from chemdataextractor.scrape.base import BaseScraper, BaseRequester, BaseFormat
from chemdataextractor.scrape.entity import EntityList
from chemdataextractor.scrape.selector import Selector
from chemdataextractor.scrape.scraper import SearchScraper, UrlScraper
from chemdataextractor.scrape.pub import rsc, acs
"A class that is derived from an abstract class cannot be instantiated unless all of its abstract methods are overridden."
"The abstract methods are make_request, process response, and get_roots taht are in the BaseScraper class"

scraper = rsc.RscSearchScraper()

#print(scraper.perform_search("MOF+CO2", 100).text) #.text is the text that is on the webpage

acs_scraper = acs.AcsSearchScraper()
