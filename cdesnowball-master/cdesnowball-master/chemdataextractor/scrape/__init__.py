# -*- coding: utf-8 -*-
"""
chemdataextractor.scrape
~~~~~~~~~~~~~~~~~~~~~~~~

Declarative scraping framework for extracting structured data from HTML and XML documents.

"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

#: Block level HTML elements
BLOCK_ELEMENTS = {
    'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol', 'pre', 'dd', 'dl', 'div', 'noscript', 'blockquote', 'form',
    'hr', 'table', 'fieldset', 'address', 'article', 'aside', 'audio', 'canvas', 'figcaption', 'figure', 'footer',
    'header', 'hgroup', 'output', 'section', 'body', 'head', 'title', 'tr', 'td', 'th', 'thead', 'tfoot', 'dt', 'li',
    'tbody',
}

#: Inline level HTML elements
INLINE_ELEMENTS = {
    'b', 'big', 'i', 'small', 'tt', 'abbr', 'acronym', 'cite', 'code', 'dfn', 'em', 'kbd', 'strong', 'samp', 'var',
    'a', 'bdo', 'br', 'img', 'map', 'object', 'q', 'script', 'span', 'sub', 'sup', 'button', 'input', 'label',
    'select', 'textarea', 'blink', 'font', 'marquee', 'nobr', 's', 'strike', 'u', 'wbr','hsp', 'inf'
}


from chemdataextractor.scrape.clean import Cleaner, clean, clean_html, clean_markup
from chemdataextractor.scrape.entity import Entity, EntityList, DocumentEntity
from chemdataextractor.scrape.fields import StringField, IntField, FloatField, BoolField, DateTimeField, EntityField, UrlField
from chemdataextractor.scrape.scraper import HtmlFormat, XmlFormat, GetRequester, PostRequester, UrlScraper, RssScraper, SearchScraper
from chemdataextractor.scrape.selector import Selector, SelectorList
from chemdataextractor.scrape.pub.nlm import NlmXmlDocument
from chemdataextractor.scrape.pub.elsevier import ElsevierHtmlDocument
from chemdataextractor.scrape.pub.acs import AcsHtmlDocument
from chemdataextractor.scrape.pub.rsc import RscHtmlDocument
from chemdataextractor.scrape.pub.springer import SpringerXmlDocument
