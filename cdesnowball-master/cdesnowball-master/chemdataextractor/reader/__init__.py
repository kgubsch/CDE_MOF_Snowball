# -*- coding: utf-8 -*-
"""
chemdataextractor.reader
~~~~~~~~~~~~~~~~~~~~~~~~

Reader classes that read a file and produce a ChemDataExtractor Document object.

"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from .acs import AcsHtmlReader
from .cssp import CsspHtmlReader
from .markup import HtmlReader, XmlReader
from .pdf import PdfReader
from .plaintext import PlainTextReader
from .rsc import RscHtmlReader
from .nlm import NlmXmlReader
from .uspto import UsptoXmlReader
from .elsevier import ElsevierHtmlReader, ElsevierXmlReader
from .springer import SpringerMaterialsHtmlReader


DEFAULT_READERS = [
    AcsHtmlReader(),
    RscHtmlReader(),
    NlmXmlReader(),
    ElsevierHtmlReader(),
    ElsevierXmlReader(),
    SpringerMaterialsHtmlReader(),
    UsptoXmlReader(),
    CsspHtmlReader(),
    XmlReader(),
    HtmlReader(),
    PdfReader(),
    PlainTextReader(),
]
